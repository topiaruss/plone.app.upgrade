from setuptools import setup, find_packages

version = '1.1.7.dev0'

setup(name='plone.app.upgrade',
      version=version,
      description="Upgrade machinery for Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='Plone upgrade migration',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.upgrade',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'Products.CMFPlacefulWorkflow',
            'Products.CMFQuickInstallerTool',
            'Products.PloneTestCase',
            'Products.kupu',
            'plone.contentrules',
            'plone.app.i18n',
            'plone.app.iterate',
            'plone.app.openid',
            'plone.app.redirector',
            'plone.app.viewletmanager',
        ]
      ),
      install_requires=[
        'setuptools',
        'borg.localrole',
        'five.localsitemanager',
        'plone.portlets',
        'plone.session',
        'plone.app.folder',
        'plone.app.portlets',
        'transaction',
        'zope.app.cache',
        'zope.component',
        'zope.interface',
        'zope.location',
        'zope.ramcache',
        'zope.site',
        'Acquisition',
        'Products.CMFPlone',
        'Products.Archetypes',
        'Products.ATContentTypes',
        'Products.contentmigration',
        'Products.CMFActionIcons',
        'Products.CMFCalendar',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.CMFDiffTool',
        'Products.CMFEditions',
        'Products.CMFFormController',
        'Products.CMFQuickInstallerTool',
        'Products.CMFUid',
        'Products.DCWorkflow',
        'Products.GenericSetup',
        'Products.MimetypesRegistry',
        'Products.PloneLanguageTool',
        'Products.PlonePAS',
        'Products.PluggableAuthService',
        'Products.PortalTransforms',
        'Products.ResourceRegistries',
        'Products.SecureMailHost', # For migration only, when can we remove this?
        'Products.ZCatalog >= 2.13.4',
        'Zope2',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
