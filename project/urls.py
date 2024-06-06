from project import views
from django.urls import path

app_name = "project"

urlpatterns=[
    path("register/", views.Register, name="register"),
    path("login/", views.user_login, name="login"),
    path("", views.groupList.as_view(), name="group"),
    path("<int:pk>/group_detail", views.Group_Detail.as_view(), name="group_detail"),
    path("<int:pk>/update", views.Group_Update.as_view(), name="group_update"),
    path("<int:pk>/delete", views.Delete_Group.as_view(), name="group_delete"),
    path("create/", views.Create_Group.as_view(), name="group_creation"), 
    path("<int:pk>/",views.send, name="detail"),
    path("getMessages/<int:pk>/", views.getMessage, name="getMessage"),
    path('request/sent/', views.request_sent, name='request_sent'),
    path('request/pending/', views.request_pending, name='request_pending'),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/approve/<int:pk>/", views.approved_request, name="approve_request"),
    path("admin/reject/<int:pk>/", views.rejected_request, name="reject_request"),
    path("send_request/<int:pk>/", views.SendRequest, name="send_request"),
    path("weather/", views.weather, name="weather"),
    path('group/<int:group_pk>/remove_member/<int:user_pk>/', views.remove_member, name='remove_member'),
    # path("username/", views.User_list.as_view(), name="user_list"),
    # path('group/<int:group_pk>/add_member/<int:user_pk>/', views.add, name='add_member'),
    path('group/<int:group_pk>/user_list/', views.User_list.as_view(), name='user_list'),
    path('group/<int:group_pk>/add_member/<int:user_pk>/', views.add, name='add_member'),


    #path("project/<int:pk>/",views.send_message, name="send"),

]