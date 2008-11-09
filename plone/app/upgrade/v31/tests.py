from zope.interface import noLongerProvides

from Products.CMFPlacefulWorkflow.interfaces import IPlacefulMarker
from Products.CMFPlone.setuphandlers import replace_local_role_manager
from Products.PlonePAS.interfaces.plugins import ILocalRolesPlugin

from plone.app.upgrade.v31.betas import reinstallCMFPlacefulWorkflow

from plone.app.upgrade.tests.base import MigrationTest


class TestMigrations_v3_1(MigrationTest):

    def afterSetUp(self):
        self.qi = self.portal.portal_quickinstaller
        self.wf = self.portal.portal_workflow
        self.ps = self.portal.portal_setup

    def testReinstallCMFPlacefulWorkflow(self):
        # first the product needs to be installed
        self.qi.installProduct('CMFPlacefulWorkflow')
        # Delete existing logs to prevent race condition
        self.ps.manage_delObjects(self.ps.objectIds())
        # We remove the new marker, to ensure it's added on reinstall
        if IPlacefulMarker.providedBy(self.wf):
            noLongerProvides(self.wf, IPlacefulMarker)
        reinstallCMFPlacefulWorkflow(self.portal, [])
        self.failUnless(IPlacefulMarker.providedBy(self.wf))

    def testReinstallCMFPlacefulWorkflowDoesNotInstall(self):
        reinstallCMFPlacefulWorkflow(self.portal, [])
        self.failIf(self.qi.isProductInstalled('CMFPlacefulWorkflow'))

    def testReinstallCMFPlacefulWorkflowNoTool(self):
        self.portal._delObject('portal_quickinstaller')
        reinstallCMFPlacefulWorkflow(self.portal, [])

    def testReplaceLocalRoleManager(self):
        # first we replace the local role manager with the one from PlonePAS
        uf = self.portal.acl_users
        # deactivate and remove the borg plugin
        uf.plugins.removePluginById('borg_localroles')
        uf.manage_delObjects(['borg_localroles'])
        # activate the standard plugin
        uf.plugins.activatePlugin(ILocalRolesPlugin, 'local_roles')
        # Bring things back to normal
        replace_local_role_manager(self.portal)
        plugins = uf.plugins.listPlugins(ILocalRolesPlugin)
        self.failUnlessEqual(len(plugins), 1)
        self.failUnlessEqual(plugins[0][0], 'borg_localroles')

    def testReplaceLocalRoleManagerTwice(self):
        # first we replace the local role manager with the one from PlonePAS
        uf = self.portal.acl_users
        # deactivate and remove the borg plugin
        uf.plugins.removePluginById('borg_localroles')
        uf.manage_delObjects(['borg_localroles'])
        # activate the standard plugin
        uf.plugins.activatePlugin(ILocalRolesPlugin, 'local_roles')
        # run the migration twice
        replace_local_role_manager(self.portal)
        replace_local_role_manager(self.portal)
        plugins = uf.plugins.listPlugins(ILocalRolesPlugin)
        self.failUnlessEqual(len(plugins), 1)
        self.failUnlessEqual(plugins[0][0], 'borg_localroles')

    def testReplaceLocalRoleManagerNoPlugin(self):
        # first we replace the local role manager with the one from PlonePAS
        uf = self.portal.acl_users
        # deactivate and remove the borg plugin
        uf.plugins.removePluginById('borg_localroles')
        uf.manage_delObjects(['borg_localroles'])
        # delete the standard plugin
        uf.manage_delObjects(['local_roles'])
        # Run the migration, which shouldn't fail even if the expected
        # plugin is missing
        replace_local_role_manager(self.portal)
        plugins = uf.plugins.listPlugins(ILocalRolesPlugin)
        self.failUnlessEqual(len(plugins), 1)
        self.failUnlessEqual(plugins[0][0], 'borg_localroles')

    def testReplaceLocalRoleManagerNoPAS(self):
        uf = self.portal.acl_users
        # delete the plugin registry
        uf._delObject('plugins')
        replace_local_role_manager(self.portal)

    def testReplaceLocalRoleManagerNoUF(self):
        # Delete the user folder
        uf = self.portal._delObject('acl_users')
        replace_local_role_manager(self.portal)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMigrations_v3_1))
    return suite
