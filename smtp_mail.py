import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mimetypes


#----- PARAMETERS -----#
# 送信設定（学内のみで利⽤可能）な状況を想定
# 以下にSMTPサーバーの情報とメールの内容を追加
smtp_server = 'smtp.hines.hokudai.ac.jp'
smtp_port = 25
smtp_username = 'XXXXX@eis.hokudai.ac.jp'  # 送信元のメールアドレス
smtp_password = ''  # 送信元のメールアドレスのパスワード

# 送信先のメールアドレスとメールの内容を指定
to_email = 'XXXXX@eis.hokudai.ac.jp'
subject = 'Test'
body = 'Test'

# 添付ファイルのパスを指定
attachment_path = 'XXXXX'
#----------------------#


def attach_file(msg, attachment_path):
    # 添付ファイルのMIMEタイプを取得
    mime_type, _ = mimetypes.guess_type(attachment_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    # MIMEBaseで添付ファイルを設定
    base = MIMEBase(*mime_type.split('/'))
    with open(attachment_path, 'rb') as file:
        base.set_payload(file.read())
    encoders.encode_base64(base)

    # ファイル名をヘッダに設定
    base.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
    
    # メッセージに添付ファイルを追加
    msg.attach(base)


# メールの送信
def send_email(subject, body, to_email, smtp_server, smtp_port, smtp_username, smtp_password, attachment_path=None):
    # メールの作成
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    # メール本文の追加
    msg.attach(MIMEText(body, 'plain'))

    # 添付ファイルの追加
    if attachment_path:
        attach_file(msg, attachment_path)

    # SMTPサーバーへの接続とメールの送信
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # TLSを使用する場合
        server.starttls()
        # ユーザー名とパスワードでログイン
        # server.login(smtp_username, smtp_password)
        # メールの送信
        server.sendmail(smtp_username, to_email, msg.as_string())


if __name__ == '__main__':
    send_email(subject, body, to_email, smtp_server, smtp_port, smtp_username, smtp_password, attachment_path)