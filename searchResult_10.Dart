import 'dart:collection';

void main() {
 print(searchResults("Ap"));
 }

List searchResults(String inString) {
  List<String> resultList = new List<String>();
  List<String> inStringList=inString.split('');
  HashMap resultVallueList = new HashMap<String,int>();
  int w=0;
 for(int i=0;i<produkts().length;i++){
   if(produkts()[i].length==inStringList.length){
     w=realResults(inStringList,produkts()[i]);
   }
   else{
     w=surrealResults(inStringList,produkts()[i]);
   }
   resultVallueList[produkts()[i]]=w;
 }
  var sortedMap = Map.fromEntries(
    resultVallueList.entries.toList()
    ..sort((e1, e2) => e1.value.compareTo(e2.value)));
  print(sortedMap);
  return sortedMap.keys.toList();
}

int realResults(List<String> inStringList,String produktString){
  List<String> produktStringList=produktString.split('');
  int nbError =0;
  for(int i=0;i<inStringList.length;i++){
    if(!(inStringList[i]==produktStringList[i])){
      nbError++;
    }
  }
   
  return nbError;
}

int surrealResults(List<String> inStringList,String produktString){
  List<String> produktStringList=produktString.split('');
  int nbCorrect =0;
  for(int i=0;i<inStringList.length;i++){
    for(int j=0;j<produktStringList.length;j++){
      if(inStringList[i]==produktStringList[j]){
        nbCorrect++;
        produktStringList.removeAt(j);
        j=produktStringList.length;
      }
    }
  }
   
  return inStringList.length-nbCorrect;
}

List <String> produkts(){
  List<String> produktList=new List<String>();
  produktList.add("Apfel");
  produktList.add("Kirsche");
  produktList.add("Toast");
  produktList.add("Banane");
  produktList.add("Milch");
  produktList.add("Ananas");
  return produktList;
}