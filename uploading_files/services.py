import datetime
from uuid import uuid4
from fastapi import HTTPException
from minio_config import client, bucket
import os
import tempfile
import mimetypes
from mongo_config import files_collection


async def upload_a_file(file, user):

    allowed_types = ["image/jpeg", "image/png", "image/gif", "video/mp4", "video/mpeg", "video/webm"]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=418,
                            detail="Invalid file type. Only .jpeg, .png, .gif, .mp4, .mpeg, .webm types are allowed!")

    file_extension = mimetypes.guess_extension(file.content_type)

    file_name = f'media/{uuid4()}{file_extension}'

    # Create a temporary file to save the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
        file_content = await file.read()
        temp_file.write(file_content)

    # Upload the temporary file to MinIO
    client.fput_object(bucket_name=bucket, object_name=file_name, file_path=temp_path, content_type=file.content_type)

    # Remove the temporary file
    os.remove(temp_path)

    get_url = client.get_presigned_url("GET", bucket_name=bucket, object_name=file_name)

    details = {
        # "_id": files_collection.find({}).sort("_id", -1)[0]["_id"] + 1,
        "_id": files_collection.count_documents({}) + 1,
        "file": get_url,
        "creator_id": user.id,
        "is_used": False,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    if file.content_type == "video/mp4" or file.content_type == "video/mpeg" or file.content_type == "video/webm":
        details["media_type"] = "video"
    else:
        details["media_type"] = "image"

    files_collection.insert_one(details)
    return details


async def get_files(skip, limit, sort_by, sorting_direction, media_type, user):

    if media_type == "all":
        files_list = files_collection.find({"media_type": {"$in": ["image", "video"]}}).limit(limit).skip(skip).\
            sort(sort_by, int(sorting_direction))
        result = [file for file in files_list]
        result.append({"total_count": files_collection.count_documents({"media_type": {"$in": ["image", "video"]}})})
        return result

    else:
        files_list = files_collection.find({"media_type": {"$in": [media_type]}}).limit(limit).skip(skip).\
            sort(sort_by, int(sorting_direction))
        result = [file for file in files_list]
        result.append({"total_count": files_collection.count_documents({"media_type": media_type})})
        return result


