import uuid

def createUniqueDjangoUsername():
    '''
        Creates a GUID based username that is compatible with 
        Django limitations
    '''
    return (str(uuid.uuid4()).translate(None, '-'))[:30]

