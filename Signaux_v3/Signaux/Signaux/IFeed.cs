using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    internal interface IFeed
    {
        public int getCurseur();
        public string[] getLines();


        public void setCurseur(int curseur);
        public void setLines(string[] lines);

    }
}
