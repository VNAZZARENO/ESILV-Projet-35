using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    public interface ISignal
    {
        // Chaque classe doit avoir un nom, une valeur, un flag iscalculated, flag isValid, une PreviousValue
        public string getName();
        public double getValue();
        public bool getIsCalculated();
        public bool getIsValid();
        public double getPreviousValue();

        public void setName(string name);
        public void setValue(double value);
        public void setIsCalculated(bool isCalculated);
        public void setIsValid(bool isValid);
        public void setPreviousValue(double PreviousValue);
        public void Calculate();
        
    }
}
