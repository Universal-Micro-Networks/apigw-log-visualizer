import argparse
import json
import os
from typing import Any

import httpx

SRC_METABASE_HOME = os.getenv("SRC_METABASE_HOME", "http://192.168.68.30:3000")
DST_METABASE_HOME = os.getenv("DST_METABASE_HOME", "http://localhost:3000")
COMMON_HEADERS = {"Content-Type": "application/json"}
DASHBOARD_ID = int(os.getenv("DASHBOARD_ID", "1"))


def login(user: str, password: str, metabase_home: str) -> str:
    """get session ID from metabase with specified user and password

    Args:
        user (str): user name (email)
        password (str): password
        metabase_home (str): metabase URL

    Returns:
        str: session ID
    """
    requset_data = {"username": user, "password": password}
    r = httpx.post(
        f"{metabase_home}/api/session", headers=COMMON_HEADERS, json=requset_data
    )
    response_data = r.json()

    return response_data["id"]


def get_dashboard_settings(session_id: str) -> dict[str, Any]:
    """get dashboard settings

    Args:
        session_id (str): session ID

    Returns:
        dict[str, Any]: dashboard settings dictionary data
    """
    http_headers = COMMON_HEADERS
    http_headers["X-Metabase-Session"] = session_id
    r = httpx.get(
        f"{SRC_METABASE_HOME}/api/dashboard/{DASHBOARD_ID}", headers=http_headers
    )
    response_data = r.json()

    return response_data


def get_card_settings(session_id: str, card_id_list: list[int]) -> list[dict[str, Any]]:
    """get card settings

    Args:
        session_id (str): session ID
        card_id_list (list[int]): card ID list to get settings

    Returns:
        list[dict[str, Any]]: List of card settings dictionary data
    """
    http_headers = COMMON_HEADERS
    http_headers["X-Metabase-Session"] = session_id
    card_json_list = []

    for card_id in card_id_list:
        r = httpx.get(f"{SRC_METABASE_HOME}/api/card/{card_id}", headers=http_headers)
        try:
            response_data = r.json()
            card_json_list.append(response_data)
        except json.decoder.JSONDecodeError:
            print(r.text)

    return card_json_list


def put_card_settings(
    session_id: str, _card_dict_list: list[dict[str, Any]]
) -> dict[int, int]:
    """put card settings

    Args:
        session_id (str): session ID
        _card_dict_list (list[dict[str, Any]]): List of card settings dictionary data

    Returns:
        dict[int, int]: card ID map from src metabase to dst metabase
    """
    _card_id_src_dst_map = {}
    http_headers = COMMON_HEADERS
    http_headers["X-Metabase-Session"] = session_id

    for _card_dict in _card_dict_list:
        r = httpx.post(
            f"{DST_METABASE_HOME}/api/card", headers=http_headers, json=_card_dict
        )
        if r.status_code > 299:
            print(r.text)
        response_data = r.json()
        _card_id_src_dst_map[_card_dict["id"]] = response_data["id"]
        with open(f"card_{response_data['id']}.json", "w", encoding="UTF-8") as f:
            json.dump(response_data, f)

    return _card_id_src_dst_map


def put_dashboard(session_id: str, _dashboard_data: dict[str, Any]) -> None:
    """put dashboard settings

    Args:
        session_id (str): session ID
        _dashboard_data (dict[str, Any]): dashboard settings dictionary data
    """
    http_headers = COMMON_HEADERS
    http_headers["X-Metabase-Session"] = session_id
    r = httpx.post(
        f"{DST_METABASE_HOME}/api/dashboard",
        headers=http_headers,
        json=_dashboard_data,
    )
    if r.status_code > 299:
        print(r.text)
        return
    response_data = r.json()
    r = httpx.put(
        f"{DST_METABASE_HOME}/api/dashboard/{response_data['id']}",
        headers=http_headers,
        json=_dashboard_data,
    )
    if r.status_code > 299:
        print(r.text)
        return

    with open("dashboard_data.json", "w", encoding="UTF-8") as f:
        json.dump(_dashboard_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--user", required=True, help="metabase user name (email)"
    )
    parser.add_argument("-p", "--password", help="password")

    args = parser.parse_args()
    old_card_id_list = []  # card ID list from src metabase

    # 1. get session id from src metabase
    src_session_id = login(args.user, args.password, SRC_METABASE_HOME)

    # 2. get dashboard settings
    dashboard_data = get_dashboard_settings(session_id=src_session_id)
    for dashcard in dashboard_data["dashcards"]:
        if "id" in dashcard["card"]:
            old_card_id_list.append(dashcard["card"]["id"])
    sorted_card_id_list = sorted(old_card_id_list)
    # 3. get card settings
    card_dict_list = get_card_settings(src_session_id, sorted_card_id_list)
    # remove collection ID to register the card in the root collection instead of the original collection
    for card_dict in card_dict_list:
        if "collection_id" in card_dict:
            card_dict["collection_id"] = None

    # 4. get session id from dst metabase
    dst_session_id = login(args.user, args.password, DST_METABASE_HOME)

    # 5. put card settings
    card_id_src_dst_map = put_card_settings(dst_session_id, card_dict_list)
    for dashcard in dashboard_data["dashcards"]:
        if "id" not in dashcard["card"]:
            continue
        new_card_id: int = 0
        if dashcard["card"]["id"] in card_id_src_dst_map:
            new_card_id = card_id_src_dst_map[dashcard["card"]["id"]]
            dashcard["card"]["id"] = new_card_id
            for parameter_mapping in dashcard["parameter_mappings"]:
                if "card_id" in parameter_mapping:
                    parameter_mapping["card_id"] = new_card_id
        else:
            print(f"card ID {dashcard['card']['id']} is not in the map")

        dashcard["card_id"] = new_card_id

    # 6. put dashboard settings
    put_dashboard(dst_session_id, dashboard_data)
