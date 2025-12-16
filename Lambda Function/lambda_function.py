import json

def lambda_handler(event, context):
    def doNow(w, l):
        w=w*2
        l=l*2
        answer=l+w
        return answer
    
    answer=doNow(int(event['w']),int(event['l']))
    
    
    return{
        'Perimeter of Rectangle': answer
    }
