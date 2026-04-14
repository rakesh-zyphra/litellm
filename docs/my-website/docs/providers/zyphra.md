import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Zyphra
https://www.zyphra.com/

**We support ALL Zyphra models, just set `zyphra/` as a prefix when sending completion requests**

## API Key
```python
# env variable
os.environ['ZYPHRA_API_KEY']
```

## Sample Usage
```python
from litellm import completion
import os

os.environ['ZYPHRA_API_KEY'] = ""
response = completion(
    model="zyphra/zaya-1",
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
)
print(response)
```

## Sample Usage - Streaming
```python
from litellm import completion
import os

os.environ['ZYPHRA_API_KEY'] = ""
response = completion(
    model="zyphra/zaya-1",
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
    stream=True
)

for chunk in response:
    print(chunk)
```

## Supported Models

| Model Name | Function Call |
|---|---|
| zaya-1 | `completion(model="zyphra/zaya-1", messages)` |
| deepseek-r1 | `completion(model="zyphra/deepseek-r1", messages)` |

## Reasoning Content

Zyphra models can return reasoning content separately from the final response. The reasoning is automatically mapped to `reasoning_content` in the response.

```python
from litellm import completion
import os

os.environ['ZYPHRA_API_KEY'] = ""

response = completion(
    model="zyphra/zaya-1",
    messages=[{"role": "user", "content": "What is 2+2?"}],
)

# Access reasoning content
print(response.choices[0].message.reasoning_content)

# Access final answer
print(response.choices[0].message.content)
```
