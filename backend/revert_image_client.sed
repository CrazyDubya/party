s/async with session.post(url, headers=headers, json=payload) as response:/response = await session.post(url, headers=headers, json=payload)/g
s/    if response.status == 200:/if response.status == 200:/g
s/    data = await response.json()/data = await response.json()/g
s/    # Runware returns image URL/# Runware returns image URL/g
s/    if data.get("data") and len(data[\"data\"]) > 0:/if data.get("data") and len(data[\"data\"]) > 0:/g
s/    image_url = data[\"data\"][0].get(\"imageURL\")/image_url = data[\"data\"][0].get(\"imageURL\")/g
s/    # Download image data/# Download image data/g
s/    image_data = await self._download_image(image_url)/image_data = await self._download_image(image_url)/g
s/    return {/return {/g
s/    else:/else:/g
s/    return {"success": False, "error": "No image data in response"}/return {"success": False, "error": "No image data in response"}/g
s/    error_text = await response.text()/error_text = await response.text()/g
s/    return {"success": False, "error": f"Runware API error: {response.status} - {error_text}"}/return {"success": False, "error": f"Runware API error: {response.status} - {error_text}"}/g
s/async with await session.get(image_url) as response:/async with session.get(image_url) as response:/g