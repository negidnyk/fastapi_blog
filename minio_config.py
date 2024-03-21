from minio import Minio

client = Minio("play.min.io",
               access_key="Q3AM3UQ867SPQQA43P2F",
               secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
               secure=True,
               )

bucket = "petblog"

found = client.bucket_exists(bucket)

if not found:

    client.make_bucket(bucket)

else:
    print(f'Bucket {bucket} already exists')

#     # Upload '/home/user/Photos/asiaphotos.zip' as object name
#     # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
#
#
# path = "C:\\Users\Артем\PycharmProjects\\fastapi_blog\media\\4_5d4f11bf-14a2-4054-89b2-e2c7606556ea.jpeg"
# file_name = 'petblog/media/users/user_id/timestampanduuid4'
#
# client.fput_object(bucket_name=bucket, object_name=file_name, file_path=path, content_type="image/jpeg")
# print("Successfully uploaded")
