from myapp import myobj
import os
#myobj.run()
port = int(os.environ.get("PORT", 5000))
myobj.run(host='0.0.0.0', port=port)
