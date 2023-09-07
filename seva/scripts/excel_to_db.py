from persons.models import Person
from vehicles.models import Vehicle
from centres.models import Centre
from departments.models import Department
import pandas as pd
import re

dict_df = pd.read_excel('C:\\Users\\JT\\Documents\\Entry_21_7_23.xlsx', sheet_name='VEHICLE_MASTER')

dict_df = dict_df.dropna(subset=['V3NUM1', 'V3NUM2'])
dict_df = dict_df.fillna('-')
for index, row in dict_df.iterrows():
    try:
        v1 = row['V3NUM1']
        v2 = row['V3NUM2']
        v2 = format(int(v2), '04d')
        id = row['V3ID']
        v = v1 + v2
        t = row['V3T']
        u = row['BADGENO'].lower()
        po = Person.objects.filter(badge=u)
        vo = Vehicle.objects.filter(vehicle_no=v)
        if len(vo) == 0 and len(po) > 0:
            if t == "SC":
                if id != "-":
                    o = Vehicle(vehicle_no=v, type="SC", custom_id=id, person=po[0])
                else:
                    o = Vehicle(vehicle_no=v, type="SC", person=po[0])
                o.save()
            if t == "CAR":
                if id != "-":
                    o = Vehicle(vehicle_no=v, type="CR", custom_id=id, person=po[0])
                else:
                    o = Vehicle(vehicle_no=v, type="CR", person=po[0])
                o.save()
            if t == "MC":
                if id != "-":
                    o = Vehicle(vehicle_no=v, type="MC", custom_id=id, person=po[0])
                else:
                    o = Vehicle(vehicle_no=v, type="MC", person=po[0])
                o.save()
            if t == "AUTO":
                if id != "-":
                    o = Vehicle(vehicle_no=v, type="AT", custom_id=id, person=po[0])
                else:
                    o = Vehicle(vehicle_no=v, type="AT", person=po[0])
                o.save()
    except Exception as err:
        print("{0} :-- {1}  {2}  {3}  {4}  {5}  {6}".format(err, v, v1, v2, u, t, id))

dict_df = dict_df.dropna(subset=['BADGENO', 'NAME', 'GENDER', 'DEPARTMENT', 'CENTRE', 'MOBILE1'])

for row in dict_df.iloc:
    b = row.to_dict()['BADGENO'].lower()
    if not re.match(r'^\w{2}\d{4}$', b):
        continue
    n = row.to_dict()['NAME'].title()
    g = row.to_dict()['GENDER'].capitalize()
    m = str(row.to_dict()['MOBILE1'])
    if not re.match(r'^\d{10}$', m):
        continue
    c = row.to_dict()['CENTRE'].lower()
    d = row.to_dict()['DEPARTMENT'].lower()
    co = Centre.objects.get(code=c)
    do = Department.objects.get(name=d)
    if g == "Male":
        g = "M"
    else:
        g = "F"
    try:
        po = Person(badge=b, type='S', centre=co, department=do, full_name=n, gender=g, contact_number=m)
        po.save()
    except Exception as err:
        print("{0} :-- {1}  {2}  {3}  {4}  {5}  {6}".format(err, b, n, g, m, c, d))