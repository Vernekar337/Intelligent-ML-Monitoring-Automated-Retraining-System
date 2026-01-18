{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7a6b1b33-f167-40a4-a216-936982b0ae7d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# logging/prediction_logger.py\n",
    "\n",
    "import json\n",
    "import datetime\n",
    "import os\n",
    "\n",
    "LOG_PATH = \"logs/prediction_logs.jsonl\"\n",
    "os.makedirs(\"logs\", exist_ok=True)\n",
    "\n",
    "def log_prediction(model_version, features, prediction):\n",
    "    record = {\n",
    "        \"timestamp\": datetime.datetime.utcnow().isoformat(),\n",
    "        \"model_version\": model_version,\n",
    "        \"features\": features,\n",
    "        \"prediction\": prediction\n",
    "    }\n",
    "\n",
    "    with open(LOG_PATH, \"a\") as f:\n",
    "        f.write(json.dumps(record) + \"\\n\")\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
