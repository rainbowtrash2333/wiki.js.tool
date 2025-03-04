import requests


class wikijs_tool:
    def __init__(self, token, url) -> None:
        self.token = token
        self.url = url

    def __format_graphql_value(self, value):
        """将 Python 值转换为 GraphQL 合法的字符串表示"""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, str):
            return f'"{value}"'
        if isinstance(value, list):
            return f'[{", ".join(self.__format_graphql_value(v) for v in value)}]'
        return str(value)

    def create_page(self, title, content, description, path, tags, editor="markdown", isPublished=True, isPrivate=False,
                    locale="zh"):

        query = f"""
                mutation Page {{
                  pages {{
                    create (
                    content: {self.__format_graphql_value(content)}, 
                    description:{self.__format_graphql_value(description)}, 
                    editor: {self.__format_graphql_value(editor)}, 
                    isPublished: {self.__format_graphql_value(isPublished)}, 
                    isPrivate: {self.__format_graphql_value(isPrivate)}, 
                    locale: {self.__format_graphql_value(locale)}, 
                    path:{self.__format_graphql_value(path)}, 
                    tags: {self.__format_graphql_value(tags)}, 
                    title:{self.__format_graphql_value(title)}) {{
                      responseResult {{
                        succeeded,
                        errorCode,
                        slug,
                        message
                      }},
                      page {{
                        id,
                        path,
                        title
                      }}
                    }}
                  }}
                }}"""
        return self.__graphql_post(query)

    def __graphql_post(self, query):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json={'query': query}
            )

            # 检查 HTTP 状态码
            response.raise_for_status()

            data = response.json()

            # 处理 GraphQL 错误
            if 'errors' in data:
                print("GraphQL Errors:")
                for error in data['errors']:
                    print(f"- {error['message']}")
                return None
            return data

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
