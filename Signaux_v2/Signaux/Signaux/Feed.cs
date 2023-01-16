using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    public class Feed
    {
        private int curseur; //Il se déplace dans le tableau lines, StreamReader ne pouvant pas être utilisé
        private string[] lines; //Le tableau contiendra les lignes du document

        public Feed(string[] lines, int curseur)
        {
            this.lines = lines;
            this.curseur = curseur;
        }

        public void setLines(string file)
        {
            lines = System.IO.File.ReadAllLines(file); //file correspondant au chemin du fichier à lire
        }

        public string[] getLines()
        {
            return lines;
        }

        public int getCurseur()
        {
            return curseur;
        }

        public void setCurseur(int Curseur)
        {
            curseur = Curseur;
        }
    }
}
