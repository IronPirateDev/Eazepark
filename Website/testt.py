def modify_withouttemp(filename, kTnum): 
    with open(filename, 'rb+') as bf: 
    try: 
        while True: 
            position = bf.tell() 
            ticket = p.load(bf) 
 if ticket['tnum'] == kTnum: 
 new_source = 
input("Enter New Source: ") 
 new_destination = 
input("Enter New Destination: ") 
 new_cost = 
float(input("Enter New Cost: ")) 
 modified_ticket = 
{'tnum': kTnum, 'source': new_source, 
'destination': new_destination, 'cost': 
new_cost} 
 bf.seek(position) 
 p.dump(modified_ticket, 
bf) 
 print("Record modified 
successfully.") 
 except EOFError: 
 print("Modifications complete.")