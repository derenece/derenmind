import socket
from maip_builder import MaipBuilder
from maip_resolver import MaipResolver
from maip_context import MaipContext

class MaipClient:
    def __init__(self, hostname = "", hostport = 0, csid = 0, clid = 0):
        self.CSID = csid
        self.CLID = clid
        self.host_name = hostname
        self.host_port = hostport
        self.context_list={}
        self.model_list = []
        self.activeModel = ""
        self.maip_socket = None

        if self.host_name != "":
            self.maip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.maip_socket.connect((self.host_name, self.host_port))
            except OSError as msg:
                self.maip_socket.close()
                self.maip_socket = None
                
    def is_connection_active(self):
        if self.maip_socket == None:
            return False
        return True

    def is_operation_available(self):
        if self.is_connection_active() == False:
            return False

        if self.CSID == 0 and self.CLID == 0:
            return False
        return True

    def get_CSID(self):
        return self.CSID

    def get_CLID(self):
        return self.CLID
    
    def get_host_name(self):
        return self.host_name

    def get_host_port(self):
        return self.host_port
    
    def get_context_list(self):
        return self.context_list
    
    def get_model_list(self):
        return self.model_list

    def create_client(self, CSID = 0, CLID = 0):
        if self.is_connection_active() == False:
            return False

        if self.CLID == 0:
            my_builder = MaipBuilder()
            my_builder.set_request_identification("INF", "inf_create_session")
            generatedData = my_builder.generate_payload()
            self.maip_socket.sendall(generatedData.encode())
            
            resultBytes = self.maip_socket.recv(16384)
            if resultBytes:
                resultString = resultBytes.decode()
                my_resolver = MaipResolver()
                my_resolver.resolve(resultString)

                if my_resolver.get_status_code() == 2002:
                    return False

                self.CSID = my_resolver.get_kval("CSID")[0]
                self.CLID = my_resolver.get_kval("CLID")[0]
                return True
        else:
            return True

    def acquire_model(self, model):
        if self.is_operation_available() == False:
            return False

        my_builder = MaipBuilder()
        my_builder.set_request_identification("INF", "inf_acquire_model")
        my_builder.set_kval("MODEL", model)
        my_builder.set_kval("CSID", self.CSID)
        my_builder.set_kval("CLID", self.CLID)
        generatedData = my_builder.generate_payload()
        self.maip_socket.sendall(generatedData.encode())
        resultBytes = self.maip_socket.recv(16384)

    def create_context(self, model, token_max):
        if self.is_operation_available() == False:
            return False
        
        my_builder = MaipBuilder()
        my_builder.set_request_identification("INF", "inf_create_context")
        my_builder.set_kval("CSID", self.CSID)
        my_builder.set_kval("CLID", self.CLID)
        my_builder.set_kval("SAMPLER", "top_k")
        my_builder.set_kval("SAMPLER", "min_p")
        my_builder.set_kval("SAMPLER", "tailfree")
        my_builder.set_kval("SAMPLER", "temp")
        my_builder.set_kval("MODEL", model)
        my_builder.set_kval("CTXLENGTH", token_max)
        generatedData = my_builder.generate_payload()
        self.maip_socket.sendall(generatedData.encode())
        resultBytes = self.maip_socket.recv(8192)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            if my_resolver.status_code != 2000:
                return False
            myCtxId = my_resolver.get_kval("CTXID")[0]
            self.context_list[myCtxId] = MaipContext(self, myCtxId, model)
            return self.context_list[myCtxId]
    
    def destroy_context(self, ctx_id):
        if self.is_operation_available() == False:
            return False
        
        my_builder = MaipBuilder()
        my_builder.set_request_identification("INF", "inf_destroy_context")
        my_builder.set_kval("CSID", self.CSID)
        my_builder.set_kval("CLID", self.CLID)


    def get_program_models(self):
        if self.is_operation_available() == False:
            return False
        
        my_builder = MaipBuilder()
        my_builder.set_request_identification("INF", "inf_get_program_models")
        my_builder.set_kval("CSID", self.CSID)
        my_builder.set_kval("CLID", self.CLID)
        generatedData = my_builder.generate_payload()
        self.maip_socket.sendall(generatedData.encode())
        resultBytes = self.maip_socket.recv(16384)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            if my_resolver.status_code != 2000:
                return False
            self.activeModel = my_resolver.get_kval("MODEL")[0]
            return my_resolver.get_kval("MODEL")
        
    def get_models(self):
        if self.is_operation_available() == False:
            return False
        
        my_builder = MaipBuilder()
        my_builder.set_request_identification("INF", "inf_get_models")
        my_builder.set_kval("CSID", self.CSID)
        my_builder.set_kval("CLID", self.CLID)
        generatedData = my_builder.generate_payload()
        self.maip_socket.sendall(generatedData.encode())
        resultBytes = self.maip_socket.recv(16384)
        if resultBytes:
            resultString = resultBytes.decode()
            my_resolver = MaipResolver()
            my_resolver.resolve(resultString)
            self.activeModel = my_resolver.get_kval("MODEL")[0]
            return my_resolver.get_kval("MODEL")