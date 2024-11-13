# File: models.py
# Author: John kim (johnjk@bu.edu), 11/11/2024
# Description: this file models the data attributes of voter analytics

from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    represents the voter model
    '''

    #  data fields
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(null=True, blank=True)
    zip_code = models.IntegerField()
    dob = models.DateField()
    dor = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''
        returns a string representation of the voter
        '''
        return f"{self.first_name} {self.last_name}"
    
def load_data():
    '''
    loads data for the voter model from the csv
    '''
    # from professor github
    Voter.objects.all().delete()
    
  
    filename = '/Users/johnkim/Downloads/newton_voters.csv'
    f = open(filename) 
    headers = f.readline() 


    for line in f:
        
        try:
            fields = line.split(',')

            voter = Voter(
                last_name = fields[1].strip(),
                first_name = fields[2].strip(),
                street_number = int(fields[3]),
                street_name = fields[4].strip(),
                apartment_number = (fields[5]) if fields[5].strip() else None,
                zip_code = int(fields[6]),
                dob = fields[7].strip(),
                dor = fields[8].strip(),
                party_affiliation = fields[9].strip(),
                precinct_number = fields[10].strip(),
                v20state = fields[11].strip() == "TRUE",
                v21town = fields[12].strip() == "TRUE",
                v21primary = fields[13].strip() == "TRUE",
                v22general = fields[14].strip() == "TRUE",
                v23town = fields[15].strip() == "TRUE",
                voter_score = int(fields[16].strip()),
            )
            print(f'Created voter: {voter}')
            voter.save() # saving/commiting to the database
        
        except:
            print(f"Exception occurred with data: last_name={fields[1].strip()}, "
                f"first_name={fields[2].strip()}, street_number={fields[3]}, "
                f"street_name={fields[4].strip()}, apartment_number={fields[5].strip() if fields[5].strip() else None}, "
                f"zip_code={fields[6]}, dob={fields[7].strip()}, dor={fields[8].strip()}, "
                f"party_affiliation={fields[9].strip()}, precinct_number={fields[10].strip()}, "
                f"v20state={fields[11].strip() == 'TRUE'}, v21town={fields[12].strip() == 'TRUE'}, "
                f"v21primary={fields[13].strip() == 'TRUE'}, v22general={fields[14].strip() == 'TRUE'}, "
                f"v23town={fields[15].strip() == 'TRUE'}, voter_score={fields[16].strip()}.")

    # after the loop
    print("Done.")
    
    
