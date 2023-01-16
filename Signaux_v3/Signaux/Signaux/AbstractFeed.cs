using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    public abstract class AbstractFeed : IFeed
    {
        public int curseur;
        public string[] lines;

        int IFeed.getCurseur()
        {
            return curseur;
        }

        string[] IFeed.getLines()
        {
            return lines;
        }

        void IFeed.setCurseur(int Curseur)
        {
            curseur = Curseur;
        }

        void IFeed.setLines(string[] Lines)
        {
            lines = Lines;
        }
    }
}
