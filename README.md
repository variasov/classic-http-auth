# Classic http auth

This package provides utils for authentication and authorization processes. Part of project "Classic".

## Authentication usage
create instance in your core level code
```python
from classic.http_auth import Authenticator

authenticator = Authenticator()
```

decorate any controller as authentication needed (parameter "authenticator" will automatically describe in the constructor)  
```python
from classic.http_auth import aaa


@component
@aaa.authenticator_needed
class Catalog:
    catalog: services.Catalog
    ...
```
decorators order is doesn't matter

choose a properly strategy in your api factory code (adapter level) and put the authenticator in the controller  

```python
from classic.http_auth import strategies as auth_strategies

from simple_shop.adapters.shop_api import authenticator

authenticator.set_strategies(
    auth_strategies.JWT(
        secret_key='123',
    )
)

controller = controllers.Catalog(
    authenticator=authenticator,
    catalog=catalog,
)
```

next step is a decorate controller method
```python
@join_point
@aaa.authenticate
def on_get_show_product(self, request, response):
    client = request.context.client
```
client appears in request.context.client  
You can pass multiple strategies to the authenticator. First succeed strategy will be winner  
If all strategies failed exception will be raised  

## Authorization usage
this stage is doing after authentication  

define groups and permissions (access schema) in your core level code and pass this one to the authenticator  
```python
from classic.http_auth import Authenticator, Group, Permission

full_control = Permission('full_control')
read_only = Permission('read_only')

groups = (
    Group('admins', permissions=[full_control]),
    Group('managers', permissions=[read_only]),
    Group('guests'),
)

authenticator = Authenticator(app_groups=groups)
```
apply authorization decorator to the controller method with needed groups and permission combination  
```python
@aaa.authenticate
@aaa.authorize(Group('admin'))
def on_get_show_product(self, request, response):
   ...
```
you can combine groups and permissions as you want
```python
@aaa.authenticate
@aaa.authorize((Group('admin') & Group('foo')) | Permission('write'))
def on_get_show_product(self, request, response):
   ...
```
if access denied exception will be raised  
