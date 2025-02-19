# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import itertools
from typing import List

from appbuilder.utils.model_util import GetModelListRequest, Models, map_model_name


def utils_get_user_agent():
    return 'appbuilder-sdk-python/{}'.format("__version__")


def get_model_list(secret_key: str = "", api_type_filter: List[str] = [], is_available: bool = False) -> list:
    """
    返回用户的模型列表。

    参数:
        secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "")。
        api_type_filter(List[str], 可选): 根据apiType过滤，["chat", "completions", "embeddings", "text2image"]，不填包括所有的。
        is_available(bool, 可选): 是否返回可用模型列表, 默认返回所有模型。

    返回:
        list: 模型列表。
    """
    request = GetModelListRequest()
    request.apiTypefilter = api_type_filter
    model = Models(secret_key=secret_key)
    response = model.list(request)
    models = []

    for model in itertools.chain(response.result.common, response.result.custom):
        if is_available and model.chargeStatus not in ["OPENED", "FREE"]:
            continue
        mapped_name = map_model_name(model.name)
        models.append(mapped_name)
    return models
