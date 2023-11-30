from realbuildapp import views
from django.urls import include, path
urlpatterns = [
    path('',views.index,name='index'),

    # ADMIN
    path('adminhome',views.adminhome,name='adminhome'),
    path('admincontractors',views.admincontractors,name='admincontractors'),
    path('admincustomers',views.admincustomers,name='admincustomers'),
    path('adminapproveuser',views.adminapproveuser,name='adminapproveuser'),
    path('viewfeedback',views.viewfeedback,name="viewfeedback"),

    # CUSTOMER
    path('customerreg',views.customerreg,name='customerreg'),
    path('customerhome',views.customerhome,name='customerhome'),
    path('customerreq',views.customerreq,name='customerreq'),
    path('assigncontractor',views.assigncontractor,name='assigncontractor'),
    path('editreq',views.editreq,name='editreq'),
    path('plandetails',views.plandetails,name='plandetails'),
    path('payment',views.payment,name="payment"),
    path('customerplanapprove',views.customerplanapprove,name="customerplanapprove"),
    path('feedback',views.feedback,name='feedback'),
    
    # CONTRACTOR
    path('contractorreg',views.contractorreg,name='contractorreg'), 
    path('contractorhome',views.contractorhome,name='contractorhome'), 
    path('contractorplan',views.contractorplan,name='contractorplan'), 
    path('contractoraddplan',views.contractoraddplan,name='contractoraddplan'),
    
    # LOGIN
    path('loginpg',views.loginpg,name='loginpg'),
    path('logout/', views.logout_view, name='logout'),
    
]

