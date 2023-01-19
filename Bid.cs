using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    public class Bid : Signal
    {
        //Constructeur à reprendre avec plus d'informations
        private Feed data; //Le tableau contiendra les lignes du document

        public Bid(Feed data)
        {
            this.data = data;
        }

        public override double Value()
        {
            string[] cut = data.getLines()[data.getCurseur()].Split(" "); //on sépare la ligne recherchée selon les différentes catégories, le ask correspond au 6ème élément
            cut[4] = cut[4].Replace('.', ','); //Rendre possible la conversion en double
            return Convert.ToDouble(cut[4]); //On return le Ask de la ligne donnée par le data.data.setCurseur()
        }

        //Fonction Avance prenant en argument un dateTime dt => Avancer le data.data.setCurseur() à l'instant juste avant dt
        public override void Avancer(DateTime dt, bool flag)
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
            //Console.WriteLine("Ce DateTime se trouve après la " + data.getCurseur() + "ème ligne");
            flag = true;
        }

        public override Feed getData()
        {
            return data;
        }

        public override void setData(Feed Data)
        {
            data = Data;
        }

        public override string getName()
        {
            return name;
        }

        public override double getValue()
        {
            return value;
        }

        public override bool getIsCalculated()
        {
            return isCalculated;
        }

        public override bool getIsValid()
        {
            return isValid;
        }

        public override void setName(string Name)
        {
            name = Name;
        }

        public override void setValue(double Value)
        {
            value = Value;
        }

        public override void setIsCalculated(bool IsCalculated)
        {
            isCalculated = IsCalculated;
        }

        public override void setIsValid(bool IsValid)
        {
            isValid = IsValid;
        }
        public override void setPreviousValue(double PreviousValue)
        {
            previousValue = PreviousValue;
        }
        public override void Calculate()
        {
            value = (!isCalculated && isValid) ? 7 * value : value;
            isCalculated = true;
        }
        public override double GetPrevious_Value()
        {
            string[] cut = data.getLines()[data.getCurseur() - 1].Split(" "); //on sépare la ligne recherchée selon les différentes catégories, le ask correspond au 6ème élément
            cut[4] = cut[4].Replace('.', ','); //Rendre possible la conversion en double
            return Convert.ToDouble(cut[4]); //On return le Ask de la ligne donnée par le data.data.setCurseur()
        }
    }
}
