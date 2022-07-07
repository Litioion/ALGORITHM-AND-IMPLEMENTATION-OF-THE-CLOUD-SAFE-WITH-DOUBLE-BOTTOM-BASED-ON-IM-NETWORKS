from pyrogram import Client
import crypto
import data


def send_file(file, mode):
    with Client("my_account", data.api_id, data.api_hash) as app:
        app.send_document("me", file, caption=f'#{mode}')


def search_message(mode):
    files = []
    with Client("my_account", data.api_id, data.api_hash) as app:
        for message in app.search_messages("me", query=f"#{mode}"):
            print(message)
            files.append({'caption': message.caption.split(' ', 1)[-1], 'message_id': message.id,
                          'file_id': message.document.file_id,
                          'file_name': message.document.file_name})
        print(files)
        return files


def download_file(file_id, file_patch, file_name, deccrypt=True):
    with Client("my_account", data.api_id, data.api_hash) as app:
        app.download_media(file_id, file_name=f'./TEMP/{file_name}')
        if deccrypt:
            crypto.decrypt(file_patch, file_name)


def delete_message(message_id):
    with Client("my_account", data.api_id, data.api_hash) as app:
        app.delete_messages('me', message_id)
