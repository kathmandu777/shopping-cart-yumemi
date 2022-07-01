
# Shopping Cart

This is a shopping-cart project for CDK development with Python.
I developed this project to learn about API gateway + Lambda + DynamoDB as a intern task at YUMEMI Inc.

## Usage
The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```sh
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```sh
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```sh
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```sh
$ poetry install
```

At this point you can now synthesize the CloudFormation template for this code.

```sh
$ cdk synth
```

To setup pre-commit

```sh
$ pre-commit install
```

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Please specify base_url when using the command (`cdk {subcommand} -c base_url="https://example.com/"`).


## API
### /login [POST]
本番環境においては別サーバーで認証をして、そのCookieを使用して本サーバーにアクセスする。今回は別サーバーがないので、仮にこのエンドポイントで認証をしている。
#### Request
```json
{
    "username": "test1",
    "password": "test1"
}
```
#### Response
cookieがセットされます。

### /carts [POST]
カートを作成する。すでにカートがある場合は、`/carts/{cart_id} [GET]` へリダイレクトされる。
#### Request
none
#### Response
```json
{"cart_id": "95ede97e3903457caa2fcf3bf719ad0b", "contents": []}
```

### /carts/{cart_id} [GET]
カートを取得する。
#### Request
none
#### Response
```json
{
    "cart_id": "95ede97e3903457caa2fcf3bf719ad0b",
    "contents": [
        {
            "variant_id": "test",
            "quantity": 3
        }
    ]
}
```


### /carts/{cart_id} [DELETE]
カートを削除する。
#### Request
none
#### Response
```json
"Cart deleted"
```

### /carts/{cart_id}/contents [PUT]
カートに商品を追加する。（冪等性などの観点からこのようなAPI形式にしました。）
#### Request
```json
{
    "contents": [
        {
            "variant_id": "test",
            "quantity": 3
        }
    ]
}
```
#### Response
```json
{
    "cart_id": "95ede97e3903457caa2fcf3bf719ad0b",
    "contents": [
        {
            "variant_id": "test",
            "quantity": 3
        }
    ]
}
```
