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

    def __build_params(self, fields_order, params):
        args = []
        for field in fields_order:
            # 只有当参数存在且不为None时才添加
            if field in params and params[field] is not None:
                value = self.__format_graphql_value(params[field])
                args.append(f"{field}: {value}")
        return ',\n      '.join(args)

    def create_page(self, **params):

        fields_order = [
            'content',
            'description',
            'editor',
            'isPublished',
            'isPrivate',
            'locale',
            'path',
            'tags',
            'title',
            'scriptCss',  # 新增参数
            'scriptJs'  # 新增参数
        ]
        params.setdefault('editor', "markdown")
        params.setdefault('isPublished', True)
        params.setdefault('isPrivate', False)
        params.setdefault('locale', "zh")

        query = f"""
                mutation Page {{
                  pages {{
                    create (
                      {self.__build_params(fields_order, params)}
                    ){{
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
            # response.raise_for_status()
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
