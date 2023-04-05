import dropbox
from dropbox.files import WriteMode
from dropbox.excetpions import ApiError, AuthError


TOKEN = ''
try:
    with open('db_token.txt', 'r') as f:
        TOKEN = f.read()
except:
    print('No TOKEN found')


def dropbox_test_token() -> bool:
    global TOKEN
    with dropbox.Dropbox(TOKEN) as dbx:
        try:
            dbx.users_get_current_account()
            return True
        except AuthError:
            return False


def dropbox_upload_file(local_path: str, dropbox_path: str, write_mode: str='overwrite') -> int:
    global TOKEN

    with dropbox.Dropbox(TOKEN) as dbx:
        with open(local_path, 'rb') as f:
            try:
                dbx.files_upload(f.read(), dropbox_path, mode=WriteMode('overwrite'))
            except AuthError as err:
                print(err)
            except ApiError as err:
                print(err)
            except Exception as err:
                print(err)
