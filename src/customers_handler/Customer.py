class Customer:
    def __init__(self, id, info, credit_info):
        '''
        Function to initialize the class
        :param id: the id of the customer
        :param info: the info of the customer
        :param credit_info: the credit info of the customer
        '''
        self.id = id
        self._info = info
        self._credit_info = credit_info
        self.status = credit_info['STATUS'].value_counts()
        self.history = credit_info.shape[0]
        self.pay_stats = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, 'C':0, 'X':0}
        self._get_pay_stats()
        self.reliability = 0
        self.bad_client = 0
        self._reliability_setted = False
        
    def __str__(self):
        return "ID: " + str(self.id) + " Status: " + str(self.status) + " history: " + str(self.history) + " History Status Reliability: " + str(self.get_history_reliability) + " Last Period Status Reliability: " + str(self.get_last_period_status_reliability)
    
    def __repr__(self):
        return "ID: " + str(self.id) + " Status: " + str(self.status) + " history: " + str(self.history) + " History Status Reliability: " + str(self.get_history_reliability) + " Last Period Status Reliability: " + str(self.get_last_period_status_reliability)
    
    def _get_pay_stats(self):
        for k in self.status.keys():
            if(k in self.status.index):
                self.pay_stats[k] = self.status[k]/self.history

    def get_history_reliability(self):        
        '''
        Function to get the reliability of the client based on the history
        :return: the reliability of the client based on the history
        '''
        if self.pay_stats['5'] > 0.05: 
            return 0
        elif self.pay_stats['4'] > 0.05:
            return 1
        elif self.pay_stats['3'] > 0.1:
            return 2
        elif self.pay_stats['3'] > 0.05 or self.pay_stats['2'] > 0.15:
            return 3
        elif self.pay_stats['2'] > 0.05 or self.pay_stats['1'] > 0.15:
            return 4
        elif self.pay_stats['1'] > 0.05 or self.pay_stats['0'] > 0.15:
            return 5
        elif self.pay_stats['0'] > 0.05 or self.pay_stats['C'] < 0.7:
            return 6
        return 7

    def get_last_period_reliability(self): 
        '''
        Function to get the reliability of the client based on the last period
        :return: the reliability of the client based on the last six months
        '''
        last_period_check = 6
        reliability = 7
        i = 0
        for _, row in self._credit_info.iterrows():
            if i == last_period_check:
                break
            if row['STATUS'] == '5' or row['STATUS'] == '4':
                return 0 
            elif row['STATUS'] == '3':
                reliability = 1
            elif row['STATUS'] == '2':
                reliability = reliability*0.35
            elif row['STATUS'] == '1':
                reliability = reliability*1.1 if reliability*1.1 < 3 else reliability*0.65
            elif row['STATUS'] == '0':
                reliability = reliability*1.2 if reliability*1.2 < 5 else reliability
            elif row['STATUS'] == 'C':
                reliability = reliability*1.25 if reliability*1.25 < 6 else reliability
            elif row['STATUS'] == 'X':
                reliability = reliability*1.35 if reliability*1.35 < 7 else 7
            i+=1
        return reliability
        
    def compute_reliability(self):
        '''
        Function to compute the reliability of the client
        '''
        self.reliability = int((self.get_history_reliability() * 0.75 + self.get_last_period_reliability() * 0.25))
        if self.reliability < 5:
            self.bad_client = 1
        self._reliability_setted = True

    def get_reliability(self):
        '''
        Function to get the reliability of the client
        :return: the reliability of the client
        '''
        if not self._reliability_setted:
            self.compute_reliability()
        return self.reliability
    
    def get_bad_client(self):
        '''
        Function to get if the client is a bad client
        :return: if the client is a bad client
        '''
        if not self._reliability_setted:
            self.compute_reliability()
        return self.bad_client

    def get_client_status(self):
        '''
        Function to get the status of the client
        '''
        return self.status
    
    def get_client_history(self):
        '''
        Function to get the history of the client
        '''
        return self.history