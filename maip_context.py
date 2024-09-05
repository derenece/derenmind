from maip_builder import MaipBuilder
from maip_resolver import MaipResolver

class MaipContext:
    
    def __init__(self, ownercl, inCtxId, inModelName):
        self.CTXID=inCtxId
        self.status_code=0
        self.owner_client = ownercl
        self.modelName = inModelName

    def get_CTXID(self):
        return self.CTXID

    def get_role(self):
        return self.role
    
    def get_status_code(self):
        return self.status_code
    
    def get_owner_client(self):
        return self.owner_client

    def reactivate_context(self):
        my_builder = MaipBuilder()
        my_builder.set_request_identification("INF", "inf_activate_context")
        my_builder.set_kval("CSID", self.owner_client.CSID)
        my_builder.set_kval("CLID", self.owner_client.CLID)
        my_builder.set_kval("CTXID", self.CTXID)
        my_builder.set_kval("MODEL", self.modelName)
        generatedData = my_builder.generate_payload()
        self.owner_client.maip_socket.sendall(generatedData.encode())
        resultBytes = self.owner_client.maip_socket.recv(16384)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            if my_resolver.status_code != 2000:
                return False
            return True

    def set_input(self, role, input_prompt):
        myRole = role
        myInput = input_prompt

        if self.owner_client.is_operation_available() == False:
            return False
        my_builder = MaipBuilder()
        my_builder.set_request_identification("EXEC", "exec_set_input")
        my_builder.set_kval("CSID", self.owner_client.CSID)
        my_builder.set_kval("CLID", self.owner_client.CLID)
        my_builder.set_kval("CTXID", self.CTXID)
        my_builder.set_kval("ROLE", myRole)
        
        generatedData = my_builder.generate_payload(myInput)
        self.owner_client.maip_socket.sendall(generatedData.encode())
        resultBytes = self.owner_client.maip_socket.recv(16384)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            if my_resolver.status_code != 3000:
                return 0

            tmpMessageId = my_resolver.get_kval("MSGID")[0]
            return tmpMessageId
    
    def execute_input(self, inMsgIds):
        if self.owner_client.is_operation_available() == False:
            return False
        
        my_builder = MaipBuilder()
        my_builder.set_request_identification("EXEC", "exec_execute_input")
        my_builder.set_kval("SAMPLER", "top_k")
        my_builder.set_kval("SAMPLER", "min_p")
        my_builder.set_kval("SAMPLER", "tailfree")
        my_builder.set_kval("SAMPLER", "temp")
        my_builder.set_kval("TOP_K", 40.0)
        my_builder.set_kval("MIN_P", 0.050)
        my_builder.set_kval("TFZ", 1.0)
        my_builder.set_kval("TEMPERATURE", 0.1)
        my_builder.set_kval("CSID", self.owner_client.CSID)
        my_builder.set_kval("CLID", self.owner_client.CLID)
        my_builder.set_kval("CTXID", self.CTXID)
        
        for ids in inMsgIds:
            my_builder.set_kval("MSGID", ids)
        
        generatedData = my_builder.generate_payload()
        self.owner_client.maip_socket.sendall(generatedData.encode())
        resultBytes = self.owner_client.maip_socket.recv(16384)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            return [my_resolver.get_data(), my_resolver.status_code]
            # my_resolver = Maip_Resolver()
            # my_resolver.resolve(resultString)
            # self.msg_id.append(my_resolver.get_kval("MSGID")[0])
            # return self.msg_id
        pass

    def execute_input_sync(self, inMsgIds):
        execResult = self.execute_input(inMsgIds)
        if execResult == False:
            return False
        outWords = execResult[0]
        execResult = self.get_next()
        while execResult[1] == 3006:
            outWords += execResult[0]
            execResult = self.get_next()
        return outWords

    def get_next(self):
        if self.owner_client.is_operation_available() == False:
            return False
        
        my_builder = MaipBuilder()
        my_builder.set_request_identification("EXEC", "exec_next")
        my_builder.set_kval("CSID", self.owner_client.CSID)
        my_builder.set_kval("CLID", self.owner_client.CLID)
        my_builder.set_kval("CTXID", self.CTXID)
        generatedData = my_builder.generate_payload()
        self.owner_client.maip_socket.sendall(generatedData.encode())
        resultBytes = self.owner_client.maip_socket.recv(16384)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            return [my_resolver.get_data(), my_resolver.status_code]

        pass
    