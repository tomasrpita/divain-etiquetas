# coding: utf-8
import os
import click
from app import create_app
app = create_app()

@app.cli.command()
@click.option("--coverage/--no-coverage", default=False)
def test(coverage):
    """
    Ejecuta los Test Unitarios con o sin reporte de Cobertura

    Recordar habilitar variables de entorno:
    > set FLASK_APP=app_name.py
    > set FLASK_ENV=development

    Para ejecutarlo SIN reporte de Cobertura:
    > flask test


    para ejecutarlo con reporte de Cobertura:
    > flask test --coverage

    """
    COV = None
    if coverage:
        import coverage

        COV = coverage.coverage(branch=True, include="app/*")
        COV.start()
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Sumario de Cobertura")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print(f"Versión HTML en: file://{covdir}/index.html")
        COV.erase()


if __name__ == "__main__":
    app.run()

