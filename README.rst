Rafi
====

A tiny route dispatcher for `Google Cloud Functions`_.

.. code-block:: python

  app = rafi.App("demo_app")

  @app.route("/hello/<name>")
  def index(name):
      return "hello {}".format(name)

.. _Google Cloud Functions: https://cloud.google.com/functions/
