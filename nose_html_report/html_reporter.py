"""A neat nose plugin to generate good-looking HTML output of a test run.
"""

# Standard library stuff
from os.path import dirname, exists, basename, realpath, join
import os
import shutil
import traceback

# Third Party plugins
import jinja2
from nose.plugins import Plugin
from pygments import highlight
from pygments.lexers import Python3TracebackLexer
from pygments.formatters import HtmlFormatter


file_dir = dirname(__file__)


#------------------------------------------------------------------------------
# HTML generator
#------------------------------------------------------------------------------
class HTMLOutputGenerator(object):
    """Generates HTML output for test results
    """

    def __init__(self):
        super(HTMLOutputGenerator, self).__init__()

    def generate(self, out_file_name, stylesheet_name, template_name, result):
        # Open and read template. Raise error on failure.
        try:
            with open(template_name, "r") as template_file:
                template = jinja2.Template(template_file.read())
        except IOError:
            raise IOError("Unable to load Jinja2 template...")

        # Make sure the directory where we write the file exists...
        out_file_name = realpath(out_file_name)
        if not exists(dirname(out_file_name)):
            os.mkdir(dirname(out_file_name))

        # Create the environment for the template
        env = {"len": len}

        # Try to write the file. Raise error on failure.
        try:
            template.stream(
                stylesheet=basename(stylesheet_name), result=result, **env
            ).dump(realpath(out_file_name))
        except Exception:
            raise Exception("Unable to render/write output...")

        dependencies = [
            # CSS
            stylesheet_name,
            join(file_dir, "html", "pygments.css"),
            join(file_dir, "html", "reset.css"),
            # JS
            join(file_dir, "html", "nosetests.js"),
            join(file_dir, "html", "jquery-2.1.1.js"),
        ]

        for file_name in dependencies:
            shutil.copyfile(
                file_name,
                join(dirname(out_file_name), basename(file_name))
            )


class Result(object):
    """Holds the list of test and statistics related to the test-run
    """

    def __init__(self):
        super(Result, self).__init__()
        self.passed = []
        self.failed = []
        self.errored = []

    @property
    def tests(self):
        return self.errored + self.failed + self.passed

    def add_success(self, test):
        self.passed.append((test, None))

    def add_failure(self, test, err):
        self.failed.append((test, err))

    def add_error(self, test, err):
        self.errored.append((test, err))

    def describe_test(self, test):
        return test.shortDescription()

    def format_error(self, err):
        if err is None:
            return ""
        exc_type, exc_val, exc_tb = err
        code = ''.join(traceback.format_exception(
            exc_type,
            exc_val if isinstance(exc_val, exc_type) else exc_type(exc_val),
            exc_tb
        ))
        return highlight(
            code, Python3TracebackLexer(), HtmlFormatter(cssclass="error-info")
        )


#------------------------------------------------------------------------------
# Nose Plugin (Frontend)
#------------------------------------------------------------------------------
class HtmlReport(Plugin):
    """Generate a HTML report for the test-run
    """
    name = "html-report"

    def options(self, parser, env=os.environ):
        super(HtmlReport, self).options(parser, env)
        parser.add_option(
            "--html-output-file",
            action="store",
            default=env.get(
                "NOSE_HTML_OUTPUT_FILE",
                join("test-report", "nosetests.html")
            ),
            dest="html_output_file",
            metavar="FILE",
            help="Produce results in the specified HTML file."
        )
        parser.add_option(
            "--html-template-file",
            action="store",
            default=env.get(
                "NOSE_HTML_TEMPLATE_FILE",
                join(file_dir, "html", "nosetests.jinja2")
            ),
            dest="html_template_file",
            metavar="FILE",
            help="Jinja2 template for generating output."
        )
        parser.add_option(
            "--html-stylesheet",
            action="store",
            default=env.get(
                "NOSE_HTML_STYLESHEET",
                join(file_dir, "html", "nosetests.css")
            ),
            dest="html_stylesheet",
            metavar="FILE",
            help="Stylesheet to use in the generated HTML file."
        )

    def configure(self, options, conf):
        super(HtmlReport, self).configure(options, conf)
        # Options
        self._out_file_name = options.html_output_file
        self._stylesheet_name = options.html_stylesheet
        self._template_name = options.html_template_file

        # Results Format: (<PASS|FAIL|ERROR>, test, error)
        self._result = Result()

    # Recording the results
    def addSuccess(self, test):
        self._result.add_success(test)

    def addFailure(self, test, err):
        self._result.add_failure(test, err)

    def addError(self, test, err):
        self._result.add_error(test, err)

    def report(self, stream):
        HTMLOutputGenerator().generate(
            self._out_file_name, self._stylesheet_name, self._template_name,
            self._result
        )

if __name__ == '__main__':

    class TestClass():
    # class TestClass():

        def test_passing(self):
            pass

        def test_failing(self):
            assert False

        def test_erroring(self):
            raise Exception()

        def test_passing_with_doc(self):
            """I'm a passing test.
            """
            pass

        def test_failing_with_doc(self):
            """I'm a failing test.
            """
            assert False

        def test_erroring_with_doc(self):
            """I'm a test that raises an error.
            """
            raise Exception()

    import nose
    pro = nose.runmodule(
        module=TestClass,
        addplugins=[HtmlReport()],
        env={"NOSE_WITH_HTML_REPORT": "True"},
        exit=False
    )
