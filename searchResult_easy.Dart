
List<String> searchResults(String inString) {
  
  List<String> resultList = new List<String>();
  List<String> produktList =produkts();      
   
  for(int i=0;i<produktList.length;i++){   
    if (produktList[i].startsWith(inString)) {
       resultList.add(produktList[i]);
    } 
  }
  return resultList;
}


List <String> produkts(){             //Beispiel Liste, JSON-Liste müsste hier importiert werden
  List<String> produktList=new List<String>();
  produktList.add("Apfel");
  produktList.add("Kirsche");
  produktList.add("Toast");
  produktList.add("Banane");
  produktList.add("Milch");
  produktList.add("Ananas");
  return produktList;
}