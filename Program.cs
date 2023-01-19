using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Signaux
{
    class Program
    {
        static void Main(string[] args)
        {
            //Lecture quand on appelle avancer => Avancer est une méthode de classe donc on est obligés de l'appeler APRES  avoir crée un feed donc ouvert un flux
            bool flagAvancer = false;
            //Appeler ou non la fonction avancer ?
            if (flagAvancer == true)
            {
                string[] list = new string[6];
                string file = "C:/Users/apote/Documents/BackUp/Cours/A4/S7/PI2/data/eurUS/2021/1 - USEUR_2021-01-03.csv";
                Feed Data = new Feed(list, 2);
                Data.setLines(file);
            }
        }

        public static List<List<object>>[] CreaCollections(params object[] list) //On passera en paramètre une liste composée de chaque objet coché et on renverra deux listes contenant les signaux d'origine et les signaux calculés
        {
            List<List<object>> TotalSignaux = new List<List<object>>();//On mettra dans l'ordre Ask, Bid, Mid, Spread
            List<List<object>> TotalSignauxCalculated = new List<List<object>>();
            foreach (object parameter in list)
            {
                List<object> Signaux = new List<object>(); //Si on avait eu le moyen d'avoir le type (sans "system." de chaque objet on aurait pu créer des listes adaptées)
                List<object> SignauxCalculated = new List<object>();

                TotalSignaux.Add(Signaux);
                TotalSignauxCalculated.Add(SignauxCalculated);
            }
            List<List<object>>[] Total = new List<List<object>>[] { TotalSignaux, TotalSignauxCalculated };
            return Total;
        } //Cette fonction crée deux collections signaux et signaux calculés pour chaque case cochée et elle renvoie un tableau contenant la liste des collections signaux et la liste des collections signaux calculés

        public static void AddList(List<List<object>> TotalSignauxCalculated, List<List<object>> TotalSignaux, Ask ask = null, Bid bid = null, Mid mid = null, Spread spread = null) 
        {
            //TotalSignaux[0] => liste de signaux de types Ask
            //TotalSignaux[1] => liste de signaux de types Bid
            //TotalSignaux[2] => liste de signaux de types Mid
            //TotalSignaux[3] => liste de signaux de types Spread
            if (ask != null)
            {
                TotalSignaux[0].Add(ask); //On l'ajoute à la première liste de signaux
                //On regarde si l'objet a son flag isCalculated et on l'ajoute à signauxclaculés si oui
                if (ask.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[0].Add(ask);//On l'ajoute à la première liste de signaux calculés si le flag isCalculated est à true
                    ask.setIsCalculated(false);//Lorsqu'un signal est ajouté à la liste de signaux calculés, ses flags sont réinitialisés à false
                    ask.setIsValid(false);
                }
            }
            if (bid != null)
            {
                TotalSignaux[1].Add(ask);
                if (bid.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[1].Add(bid);
                    bid.setIsCalculated(false);
                    bid.setIsValid(false);
                }
            }
            if (mid != null)
            {
                TotalSignaux[2].Add(ask);
                if (mid.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[2].Add(mid);
                    mid.setIsCalculated(false);
                    mid.setIsValid(false);
                }
            }
            if (spread != null)
            {
                TotalSignaux[3].Add(ask);
                if (spread.getIsCalculated() == true)
                {
                    TotalSignauxCalculated[3].Add(spread);
                    spread.setIsCalculated(false);
                    spread.setIsValid(false);
                }
            }
        } 
    }
}
