import datetime
import shortuuid

class RandomGenerator:
    @staticmethod
    def incident_id():
        prefix = "RMG"
        year = (datetime.date.today()).year        
        s = shortuuid.ShortUUID(alphabet="0123456789")
        otp = s.random(length=5)        
        id =prefix + str(otp) + str(year) 
        print("random id :", id) 
        return  id
    @staticmethod
    def user_code():
        prefix = "USER"
        year = (datetime.date.today()).year        
        s = shortuuid.ShortUUID(alphabet="0123456789")
        otp = s.random(length=6)        
        id =prefix + str(otp) + str(year) 
        print("random id :", id) 
        return  id


