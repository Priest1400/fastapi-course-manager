from passlib.context import CryptContext  # برای هش و بررسی رمز عبور

# ایجاد یک context رمزنگاری با الگوریتم bcrypt
pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

# تعریف یک کلاس برای هش کردن و بررسی رمز عبور
class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:
        # هش کردن رمز عبور با استفاده از bcrypt
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        # بررسی تطابق رمز ساده و رمز هش‌شده
        return pwd_cxt.verify(plain_password, hashed_password)
