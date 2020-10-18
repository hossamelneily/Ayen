from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from api.views import account


urlpatterns = [

    # auth_urls
    path('register', account.Register.as_view(), name="auth.register"),
    path('login', account.CustomLoginView.as_view(), name="auth.login"),
    path('logout', account.LogoutView.as_view(), name="auth.logout"),
    path('auth/api-token-auth/', obtain_jwt_token, name="auth.obtain_jwt_token"),
    path('auth/api-token-refresh/', refresh_jwt_token, name="auth.refresh_jwt_token"),

    #metadata
    path('upload-meta', account.AccountMetaData.as_view(), name='meta_upload'),
    path('list-meta', account.AccountMetaDataListAPI.as_view(), name='list_meta'),
    path('get-meta', account.AccountMetaDataDetailAPI.as_view(), name='get_meta'),

    #doc
    path('upload-doc', account.AccountUploadDocuments.as_view(), name='doc_upload'),
    path('list-doc', account.AccountDocListAPI.as_view(), name='list_doc'),
    path('get-doc', account.AccountDocDetailAPI.as_view(), name='get_doc'),

]

