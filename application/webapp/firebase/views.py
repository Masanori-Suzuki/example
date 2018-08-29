from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

import firebase_admin
from firebase_admin import auth
from firebase_admin.auth import AuthError

def index(request):
    # templateに渡す値を作る
    params = {
    }
    return render(request, 'firebase/index.html', params)

def list(request):
    # 全てのユーザー情報を取得する
    # 一回に取れるのは1000件までなので、全て取得するには、ページングが必要
    list = []
    page = auth.list_users()
    while page:
        for user in page.users:
            list.append(user.uid);
        #次の1000件を取得する
        page = page.get_next_page()

    # templateに渡す値を作る
    params = {
        'list':list,
    }
    return render(request, 'firebase/list.html', params)

def details(request, uid):
    # ユーザーデータを取得する
    # 存在しないuidで取得すると、AuthError例外が発生する
    try:
        user = auth.get_user(uid)
        # user = auth.get_user_by_email(email)
        # user = auth.get_user_by_phone_number(phone)
    except AuthError:
        return render(request, 'firebase/authError.html')

    # templateに渡す値を作る
    params = {
        'uid':          user.uid,
        'email':        user.email,
        # 'emailVerified':user.emailVerified,
        # 'phoneNumber':  user.phoneNumber,
        # 'password':     user.password,
        # 'displayName':  user.displayName,
        # 'photoURL':     user.photoURL,
        # 'disabled':     user.disabled,
    }
    return render(request, 'firebase/details.html', params)

def token(request):
    token = request.GET['token']
    print('token:' + token);

    # ID トークンを確認する
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    
    print('uid:' + uid);
    return HttpResponse("OK")

class CreateUser(TemplateView):
    def __init__(self):
        self.parames = {
        }

    def get(self, request):
        # templateに渡す値を作る
        params = {
        }
        return render(request, 'firebase/createUserInput.html', params)

    def post(self, request):
        # emailを取得する。本来は有効なメールアドレスかどうかのバリデージョンをしないと行けない
        email = request.POST['email']

        # 新しいユーザーを作成する
        user = auth.create_user(
            email=email)

        # templateに渡す値を作る
        params = {
            'uid':user.uid,
            'email':email,
        }
        return render(request, 'firebase/createUserOutput.html', params)

class UpdateUser(TemplateView):
    def __init__(self):
        self.parames = {
        }

    def get(self, request):
        uid = request.GET['uid']

        # ユーザーデータを取得する
        try:
            user = auth.get_user(uid)
        except AuthError:
            return render(request, 'firebase/authError.html')

        # templateに渡す値を作る
        params = {
            'uid':          user.uid,
            'email':        user.email,
            # 'emailVerified':user.emailVerified,
            # 'phoneNumber':  user.phoneNumber,
            # 'password':     user.password,
            # 'displayName':  user.displayName,
            # 'photoURL':     user.photoURL,
            # 'disabled':     user.disabled,
        }
        return render(request, 'firebase/UpdateUserInput.html', params)

    def post(self, request):
        uid =           request.POST['uid']
        email =         request.POST['email']
        # emailVerified = request.POST['emailVerified']
        # phoneNumber =   request.POST['phoneNumber']
        # password =      request.POST['password']
        # displayName =   request.POST['displayName']
        # photoURL =      request.POST['photoURL']
        # disabled =      request.POST['disabled']

        # ユーザーを更新する
        user = auth.update_user(
            uid,
            email=email,
            # emailVerifiedz=emailVerified,
            # phoneNumber=phoneNumber,
            # password=password,
            # displayName=displayName,
            # photoURL=photoURL,
            # disabled=disabled
        )

        # templateに渡す値を作る
        params = {
            'uid':  user.uid,
            'email':email,
        }
        return render(request, 'firebase/UpdateUserOutput.html', params)

class DeleteUser(TemplateView):
    def __init__(self):
        self.parames = {
        }

    def get(self, request):
        uid = request.GET['uid']

        # ユーザーデータを取得する
        try:
            user = auth.get_user(uid)
        except AuthError:
            return render(request, 'firebase/authError.html')

        # templateに渡す値を作る
        params = {
            'uid':  user.uid,
            'email':user.email,
        }
        return render(request, 'firebase/DeleteUserInput.html', params)

    def post(self, request):
        uid = request.POST['uid']

        # ユーザーを削除する
        auth.delete_user(uid)

        # templateに渡す値を作る
        params = {
            'uid':uid,
        }
        return render(request, 'firebase/DeleteUserOutput.html', params)
