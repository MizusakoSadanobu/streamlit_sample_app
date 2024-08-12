import pytest
from utils import hash_password, check_password

def test_hash_password():
    password = "mysecretpassword"
    hashed_password = hash_password(password)

    # ハッシュされたパスワードが元のパスワードと異なることを確認
    assert hashed_password != password

    # ハッシュされたパスワードがNoneや空でないことを確認
    assert hashed_password is not None
    assert len(hashed_password) > 0

def test_check_password():
    password = "mysecretpassword"
    hashed_password = hash_password(password)

    # 正しいパスワードでチェックが成功することを確認
    assert check_password(hashed_password, password)

    # 間違ったパスワードでチェックが失敗することを確認
    wrong_password = "wrongpassword"
    assert not check_password(hashed_password, wrong_password)
