// *****PLEASE ENTER YOUR DETAILS BELOW*****
// T6-rm-mongo.mongodb.js

// Student ID: 34550720
// Student Name: Haouxan Zhang

// Comments for your marker:

// ===================================================================================
// DO NOT modify or remove any of the comments below (items marked with //)
// ===================================================================================

// Use (connect to) your database - you MUST update xyz001
// with your authcate username

use("hzha0340");

// (b)
// PLEASE PLACE REQUIRED MONGODB COMMAND TO CREATE THE COLLECTION HERE
// YOU MAY PICK ANY COLLECTION NAME
// ENSURE that your query is formatted and has a semicolon
// (;) at the end of this answer

// Drop collection
db.collection.drop();

// Create collection and insert documents
db.collection.insertMany[
{
 "_id": 1,
 "carn_name": "RM Spring Series Clayton 2024",
 "carn_date": "22-Sep-2024",
 "team_name": "Champions",
 "team_leader": {
 "name": "Rob De Costella",
 "phone": "0422888999",
 "email": "rob@gmail.com"
 },
 "team_no_of_members": 4,
 "team_members": [
 {
 "competitor_name": "Jane Ryan",
 "competitor_phone": "0453243132",
 "event_type": "5 Km Run",
 "entry_no": 2,
 "starttime": "09:31:04",
 "finishtime": "10:02:22",
 "elapsedtime": "00:31:18"
 },
 {
 "competitor_name": "Cathy Freeman",
 "competitor_phone": "0422666777",
 "event_type": "10 Km Run",
 "entry_no": 1,
 "starttime": "08:30:57",
 "finishtime": "09:38:08",
 "elapsedtime": "01:07:11"
 },
 {
 "competitor_name": "Rob De Costella",
 "competitor_phone": "0422888999",
 "event_type": "10 Km Run",
 "entry_no": 2,
 "starttime": "08:32:05",
 "finishtime": "09:27:06",
 "elapsedtime": "00:55:01"}]
}]



// List all documents you added

db.collection.find();

// (c)
// PLEASE PLACE REQUIRED MONGODB COMMAND/S FOR THIS PART HERE
// ENSURE that your query is formatted and has a semicolon
// (;) at the end of this answer
db.team.find(
    {
        "$or":[{"team-members.event_type":/.*10 K.*/},{"team_members.event_type":/.*5 K.*/}]
    },
    {
        "_id":0, "carn_date":1, "team_members.comprtitor_name":1, "team_members.comprtitor_phone":1
    }
)




// (d)
// PLEASE PLACE REQUIRED MONGODB COMMAND/S FOR THIS PART HERE
// ENSURE that your query is formatted and has a semicolon
// (;) at the end of this answer


// (i) Add new team
db.team.insertOne({
"_id": 9527,
 "carn_name": "RM WINTER SERIES CAULFIELD 2025",
 "carn_date": "29-Jun-2025",
 "team_name": "The Great Runners",
 "team_leader": {
 "name": "Jackson Bull",
 "phone": "0422412524",
 "email": "Jackson@gmail.com"
 },
 "team_no_of_members": 1,
 "team_members": [{
 "competitor_name": "Jackson Bull",
 "competitor_phone": "0422412524",
 "event_type": "5 Km Run",
 "entry_no": 10086,
 "starttime": "-",
 "finishtime": "-",
 "elapsedtime": "-"
 }]
})



// Illustrate/confirm changes made
db.team.find({"_id":9527})




// (ii) Add new team member
db.team.updateone(
    {"_id": 6983},
    {"$push":
        {"team_members":{
            "competitor_name": "Steve Bull",
            "competitor_phone": "0422251427",
            "event_type": "10 Km Run"
        }}
    },
    {"$set":{"team_no_of_members":2}}
)




// Illustrate/confirm changes made
db.team.find({"_id":9527})

