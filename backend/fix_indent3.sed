s/^# Save image if requested/                # Save image if requested/g
s/^image_path = None/                image_path = None/g
s/^if save_path and result.get("image_data"):/                if save_path and result.get("image_data"):/g
s/^image_path = await self._save_image_file/                    image_path = await self._save_image_file/g
s/^return {/                return {/g
s/^"success": True,/                    "success": True,/g
s/^"image_data": result\["image_data"\],/                    "image_data": result["image_data"],/g
s/^"image_url": result.get("image_url"),/                    "image_url": result.get("image_url"),/g
s/^"image_path": image_path,/                    "image_path": image_path,/g
s/^"usage": usage,/                    "usage": usage,/g
s/^"prompt_used": prompt,/                    "prompt_used": prompt,/g
s/^"size": size.value,/                    "size": size.value,/g
s/^"generation_time": generation_time,/                    "generation_time": generation_time,/g
s/^"provider": provider.value/                    "provider": provider.value/g
s/^}/                }/g
s/^else:/            else:/g
s/^return result/                return result/g