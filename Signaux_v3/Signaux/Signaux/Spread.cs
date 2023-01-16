using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    public class Spread : Signal
    {
        //Constructeur à reprendre avec plus d'informations
        private Feed data; //Le tableau contiendra les lignes du document

        public Spread(Feed data)
        {
            this.data = data;
        }

        public override double Value()
        {
            string[] cut = data.getLines()[data.getCurseur()].Split(" "); //on sépare la ligne recherchée selon les différentes catégories, le ask correspond au 6ème élément
            cut[6] = cut[6].Replace('.', ','); //Rendre possible la conversion en double
            return Convert.ToDouble(cut[6]); //On return le Ask de la ligne donnée par le data.data.setCurseur()
        }

        //Fonction Avance prenant en argument un dateTime dt => Avancer le data.data.setCurseur() à l'instant juste avant dt
        public override void Avancer(DateTime dt)
        {
            List<DateTime> dates = new List<DateTime>();

            foreach (string line in data.getLines())
            {
                string[] cut = line.Split(" "); //On divise la ligne en séparant les catégories, TimeStamp correspond au 2ème élément
                if (cut[2] != "'Timestamp'")
                {
                    cut[2] = cut[2].Replace('-', '/'); //On fait en sorte d'obtenir un DateTime lisible

                    dates.Add(Convert.ToDateTime(cut[2] + " " + cut[3])); //On met tous les datetime dans une liste à part
                }
            }

            data.setCurseur(dates.IndexOf(dt)); //On trouve l'index auquel se trouve dt et on le décrémente (pas besoin de mettre -1 car on supprime la 1ère ligne)
            Console.WriteLine("Ce DateTime se trouve après la " + data.getCurseur() + "ème ligne");
        }

        public override Feed getData()
        {
            return data;
        }

        public override void setData(Feed Data)
        {
            data = Data;
        }
    }
}
