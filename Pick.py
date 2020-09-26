




class Pick():

    pick_   =   {
        #   Pick info
        'type'          :   '',
        'isLive'        :   '',
        'tipster'       :   '',
        'booker'        :   '',
        'sport'         :   '',

        #   Bet info
        'match'         :   '',
        'pick'          :   '',
        'market'        :   '',
        'bet'           :   '',
        'stake'         :   '',
        'odds'          :   '',     #   not always the same as placed

        #   Meta
        'source'        :   '',     #   pick origin (not tipster)
        'date'          :   '',
        'date_gmail'    :   '',
        'url'           :   '',
        'id_'           :   '',

        #   Economic
        'isBettable'    :   '',
        'result'        :   '',     #   win/push/lost

    }

    #   Bet info about tipster, pick and user
    tipster_annotation  =   {}

    #   In case of error, store error string
    error       =   ''

    #   Pick origin object
    pick_dict   =   None

    

    def __init__(self, dict_):
        print(dict_)
        self.pick_['_id']       =   dict_['_id']
        self.pick_['url']       =   dict_['url']
        self.pick_['tipster']   =   dict_['tipster']
        
        self.pick_['match']     =   dict_['match']
        self.pick_['pick']      =   dict_['pick']
        self.pick_['market']    =   dict_['market']
        self.pick_['bet']       =   dict_['bet']






        

    def print_pick(self):
        try:
            to_print    =   '''---------------------------------------------------------------------------------------------------------------------------------------\nMATCH: {}   \t\tTYPE: {}  \tDATE: {}  \nPICK: {}  \t  MARKET: {} - BET: {} \nStake: {}  Odds: {} \t isLive: {} \t Tipster: {}\n---------------------------------------------------------------------------------------------------------------------------------------'''.format(self.pick_['match'], self.pick_['type'], self.pick_['date'], self.pick_['pick'], self.pick_['market'], self.pick_['bet'], self.pick_['stake'], self.pick_['odds'], self.pick_['isLive'], self.pick_['tipster'])
            print(to_print)
        except Exception as e:
            print('Could not print pick ({})'.format(e))


    def bettable_pick(self):
        try:
            #   REFORMAR: hacer que lance excepción indicando la razón por la que no es apostable
            #   Comprobamos si se cumple el critterio del campo 'exc_live'
            if  self.tipster_annotation['exc_live'] and 'no_live' in self.tipster_annotation['exc_live']:
                return not self.pick_['isLive']
            elif  self.tipster_annotation['exc_live'] and 'live' in self.tipster_annotation['exc_live']:
                return self.pick_['isLive']


            #   Comprobar si el campo 'include' tiene algún deporte, en cuyo caso sólo apostamos si el deporte
            #   del pick está en la lista (distinguir live/pre) . 
            elif self.tipster_annotation['include']:
                sports  =   self.tipster_annotation['include'].split(';')
                for sp in sports:
                    #   Si el pick es de este deporte:
                    if sp.split('(')[0] in self.pick_['type']:
                        if 'no_live' in sp and not self.pick_['isLive']:
                            return True
                        elif 'live' in sp and self.pick_['isLive']:
                            return True
                            
                return False

            #   Si 'include' está vacío, comprobamos que el deporte del pick no esté en la lista de 'exclude'
            elif self.tipster_annotation['exclude']:
                sports  =   self.tipster_annotation['exclude'].split(';')
                for sp in sports:
                    if sp.split('(')[0] in self.pick_['type']:
                        if 'no_live' in sp and not self.pick_['isLive']:
                                return False
                        elif 'live' in sp and self.pick_['isLive']:
                            return False
                return True

            return True

        except Exception as e:
            raise e




    def verify(self):
        print('Verifying pick...')
        #   If not bettable pick, it throws an exception (generate pick error)
        #   Check tipster, market, bookie :
        if self.pick_['type'] in ['combo_pick', 'captcha', 'no_pick']:
            self.error  =   'Not pick message: {}'.format(self.pick_['type'])
            raise Exception('Not pick message: {}'.format(self.pick_['type']))


        elif self.pick_['type'] in ['scully_info']:
            raise Exception('Scully info message: {}'.format(self.msg['snippet']))


        elif self.pick_['type'] in ['test']:
            return True


        elif self.pick_['booker'] not in ['Bet365']:
            self.error  =   'not Bet365 pick: {}'.format(self.pick_['booker'])
            raise Exception('Not Bet365 pick: {}'.format(self.pick_['booker']))


        elif self.pick_['tipster'] not in googlesheets.get_tipsters():
            #   Not bettable picks are returned as usual (not raise exception), but server does not send them over sockets
            self.error  =   'Not bettable tipster: {}'.format(self.pick_['tipster'])
            print('Not bettable pick from {} ({}; {})'.format(self.pick_['tipster'],self.pick_['match'], self.pick_['pick']))
            self.pick_['isBettable']    =   False
            return True

        elif not self.pick_['bet'] or not self.pick_['market']:
            raise Exception('Not implemented market: {}'.format(self.pick_['market']))

        else:
            #   set annotation to check pick bettability (for picks from bettable tipsters) . 
            self.tipster_annotation         =   googlesheets.get_tipster_annotation(self.pick_['tipster'])

            if self.bettable_pick():
                print('BETTABLE PICK')
                self.pick_['isBettable']    =   True
                return True
                
            else:
                print('NOT BETTABLE PICK')
                self.pick_['isBettable']    =   False
                raise Exception('Not bettable pick')



    def check_pick(self, driver):
        if self.pick['booker']:
            return None


        driver.get(self.pick['url'])


        div_element =   driver.find_element_by_xpath('//div[contains(@class, "labels")]')
        print(div_element.get_attribute('innerHTML').strip())


        input()
