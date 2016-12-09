from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<company>[0-9a-zA-Z_-]+)/room/(?P<room_name>[0-9a-zA-Z_-]+)/$', 'rest_service.views.room_by_company',
        name='api-room'),
    url(r'^company_room/$', 'rest_service.views.room_by_company_filter', name='api-room-filter'),
    url(r'^room_user_list/(?P<username>[0-9a-zA-Z_-]+)/$', 'rest_service.views.room_by_user_list',
        name='api-room_room_user_list'),
    url(r'^room_user/(?P<username>[0-9a-zA-Z_-]+)/$', 'rest_service.views.room_by_user', name='api-room_room_user'),
    url(r'^create_room/$', 'rest_service.views.create_room_by_company', name='api-createroom'),
    url(r'^(?P<company>[0-9a-zA-Z_-]+)/users/$', 'rest_service.views.users_by_company', name='api-company-profile'),
    url(r'^(?P<company>[0-9a-zA-Z_-]+)/users/(?P<search>[0-9a-zA-Z_-]+)/$', 'rest_service.views.users_by_company',
        name='api-company-profile-search'),
    url(r'^(?P<company>[0-9a-zA-Z_-]+)/users-logged/$', 'rest_service.views.users_logged', name='api-user-logged'),

    url(r'^profile/(?P<username>[0-9a-zA-Z_-]+)/$', 'rest_service.views.profile_by_username', name='api-profile'),
    url(r'^profile/(?P<username>[0-9a-zA-Z_-]+)/path/$', 'rest_service.views.get_url_user_path',
        name='api-profile-path'),
    url(r'^profile/(?P<username>[0-9a-zA-Z_-]+)/change/$', 'rest_service.views.change_user',
        name='api-profile-username-change'),
    url(r'^profile/(?P<username>[0-9a-zA-Z_-]+)/password/$', 'rest_service.views.change_pass',
        name='api-profile-pass-change'),
    url(r'^profile/(?P<username>[0-9a-zA-Z_-]+)/email/$', 'rest_service.views.change_email',
        name='api-profile-email-change'),

    url(r'^files/upload/(?P<from_user>[0-9a-zA-Z_-]+)/$', 'rest_service.views.save_files', name='api-files-save'),
    url(r'^files/comment/(?P<file_slug>[0-9a-zA-Z_-]+)/$', 'rest_service.views.get_comments_files',
        name='api_file_comment'),
    url(r'^files/share/(?P<slug>[0-9a-zA-Z_-]+)/$', 'rest_service.views.share_file',
        name='api_file_share'),
    url(r'^files/detail/(?P<file>[0-9a-zA-Z_-]+)/$', 'rest_service.views.get_details_file', name='api-file-detail'),
    url(r'^files/detail/(?P<file>[0-9a-zA-Z_-]+)/(?P<user_post>[0-9a-zA-Z_-]+)/$',
        'rest_service.views.get_details_file', name='api-file-add-comment'),
    url(r'^files/delete/(?P<slug>[0-9a-zA-Z_-]+)/$', 'rest_service.views.delete_file', name='api_file_delete'),
    url(r'^files/(?P<username>[0-9a-zA-Z_-]+)/get/(?P<type>[a-z_]+)/$',
        'rest_service.views.get_files', name='api-files'),
    url(r'^files/(?P<username>[0-9a-zA-Z_-]+)/(?P<type>[a-z_]+)/(?P<company>[0-9a-zA-Z_-]+)/$',
        'rest_service.views.get_files', name='api-files-company'),
    url(r'^files/(?P<username>[0-9a-zA-Z_-]+)/$', 'rest_service.views.get_files', name='api-files-company'),

    url(r'^snippet/languages/$', 'rest_service.views.snippet_languages', name='create_snippet'),
    url(r'^snippet/create/$', 'rest_service.views.snippet_create', name='create_snippet'),

    url(r'^messages/(?P<username>[0-9a-zA-Z_-]+)/(?P<page>[0-9]+)$', 'rest_service.views.get_message_by_user_recent',
        name='api-message'),
    url(r'^cummunication_me/(?P<username>[0-9a-zA-Z_-]+)$', 'rest_service.views.get_comunicaton_me',
        name='api-unread'),
    url(r'^checkreaded$', 'rest_service.views.check_readed_me', name='api-checkread'),
    url(r'^resent/(?P<username>[0-9a-zA-Z_-]+)/$', 'rest_service.views.get_recente_message_user',
        name='api-recente_message_use'),
    url(r'^usercomapny$', 'rest_service.views.get_user_by_company', name='api-usercomapny$')
    ,

]
