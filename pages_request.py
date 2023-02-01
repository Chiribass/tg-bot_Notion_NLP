import requests
import json


class Pages:
    def __init__(self):
        self.url = "https://api.notion.com/v1/"

        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def search_in_db(self, db_id=""):  # TODO: сделать для бд по выбору
        url = self.url + f"databases/{self.db_id}/query"
        params = {
            "filter": {
                "property": "Type",
                "multi_select": {"contains": "test"},
            }
        }
        r = requests.post(url, headers=self.headers, json=params)
        print(r.status_code)
        json_data = r.json()
        with open(
            "./search_db_json.json", "w"
        ) as f:
            json.dump(json_data, f, indent=4)
        # FIXME: с такими атрибутами не то получается. посмотреть примеры как их реализовывать
        self.results = json_data["results"]
        print("ответ загружен")

    def search(self):
        url = self.url + "search"
        params = {
            "query": "v",
        }
        r = requests.post(url, headers=self.headers, json=params)
        print(r.status_code)
        json_data = r.json()
        with open("./search_json.json", "w") as f:
            json.dump(json_data, f, indent=4)
        print("ответ загружен")

    def add_page(self, name: str):
        url = self.url + "pages"
        params = {
            "parent": {
                "database_id": self.db_id,
            },
            "properties": {
                "Name": {"title": [{"text": {"content": name}}]},
                "Type": {"multi_select": [{"name": "test"}]},
            },
        }
        r = requests.post(url, headers=self.headers, json=params)
        print(r.status_code)
        json_data = r.json()
        # FIXME: с такими атрибутами не то получается. посмотреть примеры как их реализовывать
        self.new_page_url = json_data["url"]

        with open("./post_json.json", "w") as f:
            json.dump(json_data, f, indent=4)

        print("ответ загружен")
        # return json_data["url"]

    def add_content(self, page_id, content):
        url = self.url + f"blocks/{page_id}/children"
        params = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]},
                },
            ]
        }
        r = requests.patch(url, headers=self.headers, json=params)
        print(r.status_code)
        print(r.url)
        json_data = r.json()

        with open("./content_json.json", "w") as f:
            json.dump(json_data, f, indent=4)
        print("ответ загружен")


if __name__ == "__main__":
    post = Pages()
    post.search_in_db()
