import asyncio
import json


async def write_to_file(file, task_dict):
    all_keys = []
    placeholder_count = 0
    try:
        for key in task_dict:
            print(f"Waiting for task #{key}")
            await task_dict[key]
            result = task_dict[key].result()
            if len(result) == 0:
                print("Skipping empty result")
                continue
            print(f"Result: {result}")
            title = f"placeholder_{placeholder_count}"
            if "address" in result:
                title = result["address"]
                if (title in all_keys):
                    title += f"_{placeholder_count}"
                    placeholder_count += 1
                all_keys.append(title)
            file.write(f'"{title}": {json.dumps(result, indent=4, ensure_ascii=False)}, \n')
    except:
        return False
    return True
