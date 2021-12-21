# Classic http auth

This package provides utils for authentication and authorization processes. Part of project "Classic".

## Authentication usage
```python
from classic.http_auth import authenticate


@join_point
@authenticate
def on_get_show_product(self, request, response):
    client = request.context.client
```
Client appears in request.context.client  

For this you need to create instance in your core level code
```python
from classic.http_auth import Authenticator

authenticator = Authenticator()
```

Decorate any controller as authentication needed (parameter "authenticator" will automatically describe in the constructor)  
```python
from classic.http_auth import authenticator_needed


@component
@authenticator_needed
class Catalog:
    catalog: services.Catalog
    ...
```
Decorators order is doesn't matter

Choose a properly strategy in your api factory code (adapter level) and put the authenticator in the controller  

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

You can pass multiple strategies to the authenticator. First succeed strategy will be winner  
If all strategies failed exception will be raised  

## Authorization usage
This stage is doing after authentication  

Define groups and permissions (access schema) in your core level code and pass this one to the authenticator  
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
Apply authorization decorator to the controller method with needed groups and permission combination  
```python
from classic.http_auth import Group, authenticate


@authenticate
@authorize(Group('admin'))
def on_get_show_product(self, request, response):
   ...
```
You can combine groups and permissions as you want
```python
from classic.http_auth import Group, Permission, authenticate, authorize


@authenticate
@authorize((Group('admin') & Group('foo')) | Permission('write'))
def on_get_show_product(self, request, response):
   ...
```
If access denied exception will be raised  

## Dependencies
falcon for pushing client info through HTTP  
pyjwt for strategies  

## Tests and development mode
You can use dummy strategy
```python
auth_strategy = auth_strategies.JWT(secret_key='123')
auth_dummy_strategy = auth_strategies.Dummy(
    login=login,
    name=name,
    groups=groups,
    email=email
)

if not is_dev:
    authenticator.set_strategies(auth_strategy)
else:
    authenticator.set_strategies(auth_dummy_strategy)
```
Dummy auth data appear in a client
