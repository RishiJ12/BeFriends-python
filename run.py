from myapp import myobj
import os
#myobj.run()
port = int(os.environ.get("PORT"))
myobj.run(host='0.0.0.0', port=port)
