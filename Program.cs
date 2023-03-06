using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Signaux
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] list = new string[6];
            string file = "C:/Users/apote/Documents/BackUp/Cours/A4/S7/PI2/data/eurUS/2021/2 - USEUR_2021-01-04.csv";
            Feed Data = new Feed(list, 0); //Sous-jacent
            Data.setLines(file);

            //On suppose pour le test que la case ask a été cochée, mais tous les objets seront intialisés à null
            Ask ask = new Ask(Data);
            Bid bid = null;
            Mid mid = null;
            Spread spread = null;

            //On ne garde que les données entre 8h et 20h
            List<DateTime> liste = ClearData("C:/Users/apote/Documents/BackUp/Cours/A4/S7/PI2/data/eurUS/2021/2 - USEUR_2021-01-04.csv");

            Backtest(liste, ask, bid, mid, spread); //On lance le backtest sur les données entre 8h et 20h

            //Console.WriteLine(" Done");
        }

        public static List<List<object>>[] CreaCollections(object[] list) //On passera en paramètre une liste composée de chaque objet coché et on renverra deux listes contenant les signaux d'origine et les signaux calculés
        {
            List<List<object>> TotalSignaux = new List<List<object>>();//On mettra dans l'ordre Ask, Bid, Mid, Spread
            List<List<object>> TotalSignauxCalculated = new List<List<object>>();
            foreach (object parameter in list)
            {
                if(parameter != null)
                {
                    List<object> Signaux = new List<object>(); //Si on avait eu le moyen d'avoir le type (sans "system." de chaque objet on aurait pu créer des listes adaptées)
                    List<object> SignauxCalculated = new List<object>();

                    TotalSignaux.Add(Signaux);
                    TotalSignauxCalculated.Add(SignauxCalculated);
                }
            }
            List<List<object>>[] Total = new List<List<object>>[] { TotalSignaux, TotalSignauxCalculated };
            //Total[0] => Liste de signaux calculés au total
            //Total[0][0] => 
            return Total;
        } //Cette fonction crée deux collections signaux et signaux calculés pour chaque case cochée et elle renvoie un tableau contenant la liste des collections signaux et la liste des collections signaux calculés

        public static void AddList(List<List<object>> TotalSignaux, List<List<object>> TotalSignauxCalculated, Ask ask, Bid bid, Mid mid, Spread spread) //On ne peut pas prendre en paramètre une liste d'objets car cela nous aurait empêché de modifier les flags
        {
            //TotalSignaux[0] => liste de signaux de types Ask
            //TotalSignaux[1] => liste de signaux de types Bid
            //TotalSignaux[2] => liste de signaux de types Mid
            //TotalSignaux[3] => liste de signaux de types Spread
            if (ask != null)
            {
                //On regarde si l'objet a son flag isCalculated et on l'ajoute à signauxclaculés si oui
                if (ask.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[0].Add(ask);//On l'ajoute à la première liste de signaux calculés si le flag isCalculated est à true
                    ask.setIsCalculated(false);//Lorsqu'un signal est ajouté à la liste de signaux calculés, ses flags sont réinitialisés à false
                    ask.setIsValid(false);
                }
                else
                {
                    TotalSignaux[0].Add(ask); //On l'ajoute à la première liste de signaux
                }
            }
            if (bid != null)
            {
                if (bid.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[1].Add(bid);
                    bid.setIsCalculated(false);
                    bid.setIsValid(false);
                }
                else
                {
                    TotalSignaux[1].Add(bid); //On l'ajoute à la première liste de signaux
                }
            }
            if (mid != null)
            {
                if (mid.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[2].Add(mid);
                    mid.setIsCalculated(false);
                    mid.setIsValid(false);
                }
                else
                {
                    TotalSignaux[2].Add(mid); //On l'ajoute à la première liste de signaux
                }
            }
            if (spread != null)
            {
                if (spread.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[3].Add(spread);
                    spread.setIsCalculated(false);
                    spread.setIsValid(false);
                }
                else
                {
                    TotalSignaux[3].Add(spread); //On l'ajoute à la première liste de signaux
                }
            }
        }

        public static List<DateTime> ClearData(string file)//Ne conserve que les données entre 8h et 20h
        {
            string[] reader = System.IO.File.ReadAllLines(file);
            List<DateTime> Timestamps = new List<DateTime>();

            string[] day = reader[1].Split(' ');
            string start = day[2] + " 08:00:00";
            string end = day[2] + " 08:03:00";

            DateTime startDate = Convert.ToDateTime(start);
            DateTime endDate = Convert.ToDateTime(end); //les start et end sont le jour même à 8h et 20h

            foreach (string line in reader)
            {
                string[] values = line.Split(' ');
                if (values[2] != "'Timestamp'") //On retire la première ligne
                {
                    string fusion = values[2] + " " + values[3];
                   
                    DateTime fusiondate = Convert.ToDateTime(fusion);

                    if ((DateTime.Compare(fusiondate, startDate) >= 0) && (DateTime.Compare(fusiondate, endDate) <= 0)) //On vérifie que la date prise en compte se situe entre 8h et 20h (donc = 1 pour startDate et -1 pour endDate)
                    {
                        Timestamps.Add(fusiondate);
                    }
                }
            }
            return Timestamps;
        }


        public static void Backtest(List<DateTime> Dates, Ask ask, Bid bid, Mid mid, Spread spread) //Liste de dates entre 8h et 20h
        {
            
            object[] items = { ask, bid, mid, spread };

            //On crée les listes de signaux et de signaux calculés
            List<List<object>>[] CollectionSignaux = CreaCollections(items);

            foreach (DateTime dt in Dates) //On applique la fonction avancer sur les DateTimes
            {
                bool flag = false;
                Console.WriteLine(dt + " ");

                if (ask != null)
                {
                    ask.Avancer(dt, flag); //Placer le curseur juste avant le DateTime indiqué
                    AddList(CollectionSignaux[0], CollectionSignaux[1], ask, null, null, null); //On l'ajoute dans la liste "signaux"
                    ask.setIsValid(true);
                    Console.WriteLine("ask before = " + ask.getValue(true)); //Valeur initiale
                    ask.Calculate(); //Le flag isCalculated passe de false à true
                    Console.WriteLine("ask after = " + ask.getValue(false));//Valeur après Calculate
                    AddList(CollectionSignaux[0], CollectionSignaux[1], ask, null, null, null); //Ajouté à la liste "signaux calculés"
                    ask.setIsCalculated(false);
                    Console.WriteLine(" ");
                }
                if (bid != null)
                {
                    flag = false; //Pour vérifier que l'avancement a été fait
                    bid.Avancer(dt, flag); //Placer le curseur juste avant le DateTime indiqué
                    AddList(CollectionSignaux[0], CollectionSignaux[1], null, bid, null, null); //On l'ajoute dans la liste "signaux"
                    bid.setIsValid(true);
                    bid.Calculate(); //Le flag isCalculated passe de false à true
                    AddList(CollectionSignaux[0], CollectionSignaux[1], null, bid, null, null);
                    bid.setIsCalculated(false);
                }
                if (mid != null)
                {
                    flag = false; //Pour vérifier que l'avancement a été fait
                    mid.Avancer(dt, flag); //Placer le curseur juste avant le DateTime indiqué
                    AddList(CollectionSignaux[0], CollectionSignaux[1], null, null, mid, null); //On l'ajoute dans la liste "signaux"
                    mid.setIsValid(true);
                    mid.Calculate(); //Le flag isCalculated passe de false à true
                    AddList(CollectionSignaux[0], CollectionSignaux[1], null, null, mid, null); //Ajouté à la liste "signaux calculés"
                    mid.setIsCalculated(false);
                }
                if (spread != null)
                {
                    flag = false; //Pour vérifier que l'avancement a été fait
                    spread.Avancer(dt, flag); //Placer le curseur juste avant le DateTime indiqué
                    AddList(CollectionSignaux[0], CollectionSignaux[1], null, null, mid, null); //On l'ajoute dans la liste "signaux"
                    spread.setIsValid(true);
                    spread.Calculate(); //Le flag isCalculated passe de false à true
                    AddList(CollectionSignaux[0], CollectionSignaux[1], null, null, null, spread); //Ajouté à la liste "signaux calculés"
                    spread.setIsCalculated(false);
                }
            }
        }
    }
}
