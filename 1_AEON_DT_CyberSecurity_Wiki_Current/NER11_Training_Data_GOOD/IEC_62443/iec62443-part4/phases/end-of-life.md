# Phase 7: Product End-of-Life

**Objective:** Manage secure disposal and end-of-life for IACS products.

## End-of-Life Management Process

### Product Lifecycle Planning
```javascript
// Product End-of-Life Management System
class ProductEndOfLifeManager {
  constructor() {
    this.products = new Map();
    this.lifecyclePolicies = new Map();
    this.disposalProcedures = new Map();
    this.notificationTemplates = new Map();
  }

  // Register product
  registerProduct(productId, productInfo) {
    this.products.set(productId, {
      id: productId,
      name: productInfo.name,
      version: productInfo.version,
      releaseDate: productInfo.releaseDate,
      supportEndDate: productInfo.supportEndDate,
      endOfLifeDate: productInfo.endOfLifeDate,
      lifecycleStatus: this.calculateLifecycleStatus(productInfo),
      customers: productInfo.customers || [],
      securityUpdates: productInfo.securityUpdates || []
    });
  }

  // Calculate lifecycle status
  calculateLifecycleStatus(productInfo) {
    const now = new Date();

    if (now > productInfo.endOfLifeDate) {
      return 'end_of_life';
    } else if (now > productInfo.supportEndDate) {
      return 'extended_support';
    } else {
      return 'active_support';
    }
  }

  // Plan end-of-life process
  async planEndOfLife(productId, eolConfig) {
    const product = this.products.get(productId);
    if (!product) {
      throw new Error(`Product ${productId} not found`);
    }

    const eolPlan = {
      productId: productId,
      announcementDate: eolConfig.announcementDate,
      lastSupportDate: eolConfig.lastSupportDate,
      endOfLifeDate: eolConfig.endOfLifeDate,
      migrationPath: eolConfig.migrationPath,
      disposalProcedures: eolConfig.disposalProcedures,
      communicationPlan: eolConfig.communicationPlan,
      status: 'planned'
    };

    // Validate EOL plan
    await this.validateEOLPlan(eolPlan);

    // Store EOL plan
    product.eolPlan = eolPlan;

    // Schedule notifications
    await this.scheduleEOLNotifications(eolPlan);

    return eolPlan;
  }

  // Validate EOL plan
  async validateEOLPlan(plan) {
    const now = new Date();

    // Check dates are in correct order
    if (plan.announcementDate >= plan.lastSupportDate ||
        plan.lastSupportDate >= plan.endOfLifeDate) {
      throw new Error('EOL dates must be in chronological order');
    }

    // Check announcement is not in the past
    if (plan.announcementDate < now) {
      throw new Error('Announcement date cannot be in the past');
    }

    // Validate migration path exists
    if (!plan.migrationPath || !plan.migrationPath.targetProduct) {
      throw new Error('Migration path must be specified');
    }

    // Check disposal procedures are defined
    if (!plan.disposalProcedures || plan.disposalProcedures.length === 0) {
      throw new Error('Disposal procedures must be defined');
    }
  }

  // Schedule EOL notifications
  async scheduleEOLNotifications(plan) {
    const notifications = [
      {
        type: 'pre_announcement',
        date: new Date(plan.announcementDate.getTime() - 90 * 24 * 60 * 60 * 1000), // 90 days before
        template: 'eol_pre_announcement'
      },
      {
        type: 'announcement',
        date: plan.announcementDate,
        template: 'eol_announcement'
      },
      {
        type: 'last_support_warning',
        date: new Date(plan.lastSupportDate.getTime() - 30 * 24 * 60 * 60 * 1000), // 30 days before
        template: 'eol_support_warning'
      },
      {
        type: 'end_of_life',
        date: plan.endOfLifeDate,
        template: 'eol_final'
      }
    ];

    for (const notification of notifications) {
      await this.scheduleNotification(notification, plan);
    }
  }

  // Schedule individual notification
  async scheduleNotification(notification, plan) {
    // Implementation would schedule notification in job queue
    console.log(`Scheduled ${notification.type} notification for ${plan.productId} on ${notification.date}`);
  }

  // Execute EOL process
  async executeEndOfLife(productId) {
    const product = this.products.get(productId);
    if (!product || !product.eolPlan) {
      throw new Error(`No EOL plan found for product ${productId}`);
    }

    const plan = product.eolPlan;
    plan.status = 'executing';

    try {
      // Send final notifications
      await this.sendFinalNotifications(plan);

      // Disable new deployments
      await this.disableNewDeployments(productId);

      // Execute customer migrations
      await this.executeCustomerMigrations(plan);

      // Secure data disposal
      await this.executeDataDisposal(plan);

      // Archive product information
      await this.archiveProductInformation(productId);

      // Update product status
      product.lifecycleStatus = 'end_of_life';
      plan.status = 'completed';
      plan.completionDate = new Date();

    } catch (error) {
      plan.status = 'failed';
      plan.error = error.message;
      throw error;
    }

    return plan;
  }

  // Send final notifications
  async sendFinalNotifications(plan) {
    const template = this.notificationTemplates.get('eol_final');
    const customers = await this.getProductCustomers(plan.productId);

    for (const customer of customers) {
      await this.sendNotification(customer, template, plan);
    }
  }

  // Disable new deployments
  async disableNewDeployments(productId) {
    // Implementation would disable product in deployment systems
    console.log(`Disabled new deployments for ${productId}`);
  }

  // Execute customer migrations
  async executeCustomerMigrations(plan) {
    const customers = await this.getProductCustomers(plan.productId);

    for (const customer of customers) {
      await this.initiateMigration(customer, plan.migrationPath);
    }
  }

  // Execute data disposal
  async executeDataDisposal(plan) {
    for (const procedure of plan.disposalProcedures) {
      await this.executeDisposalProcedure(procedure, plan.productId);
    }
  }

  // Archive product information
  async archiveProductInformation(productId) {
    const product = this.products.get(productId);

    // Implementation would archive product data securely
    console.log(`Archived information for ${productId}`);
  }

  // Utility methods
  async getProductCustomers(productId) {
    const product = this.products.get(productId);
    return product.customers;
  }

  async sendNotification(customer, template, plan) {
    // Implementation would send notification to customer
    console.log(`Sent ${template} notification to ${customer.id} for ${plan.productId}`);
  }

  async initiateMigration(customer, migrationPath) {
    // Implementation would initiate migration process
    console.log(`Initiated migration for customer ${customer.id} to ${migrationPath.targetProduct}`);
  }

  async executeDisposalProcedure(procedure, productId) {
    // Implementation would execute disposal procedure
    console.log(`Executed disposal procedure ${procedure.type} for ${productId}`);
  }

  // Reporting
  generateEOLReport() {
    const products = Array.from(this.products.values());
    const activeEOL = products.filter(p => p.eolPlan && p.eolPlan.status !== 'completed');

    return {
      generated: new Date(),
      totalProducts: products.length,
      activeEOLProcesses: activeEOL.length,
      completedEOLProcesses: products.filter(p => p.lifecycleStatus === 'end_of_life').length,
      upcomingEOL: this.getUpcomingEOL(products),
      eolPlans: activeEOL.map(p => p.eolPlan)
    };
  }

  getUpcomingEOL(products) {
    const now = new Date();
    const thirtyDaysFromNow = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

    return products
      .filter(p => p.endOfLifeDate && p.endOfLifeDate <= thirtyDaysFromNow && p.endOfLifeDate > now)
      .map(p => ({
        productId: p.id,
        name: p.name,
        endOfLifeDate: p.endOfLifeDate,
        daysUntilEOL: Math.ceil((p.endOfLifeDate - now) / (24 * 60 * 60 * 1000))
      }))
      .sort((a, b) => a.endOfLifeDate - b.endOfLifeDate);
  }
}

// Example EOL management
const eolManager = new ProductEndOfLifeManager();

// Register product
eolManager.registerProduct('product1', {
  name: 'Legacy SCADA System',
  version: '1.0',
  releaseDate: new Date('2010-01-01'),
  supportEndDate: new Date('2025-12-31'),
  endOfLifeDate: new Date('2026-12-31'),
  customers: [
    { id: 'customer1', name: 'Manufacturing Corp' },
    { id: 'customer2', name: 'Utility Company' }
  ]
});

// Plan EOL
const eolPlan = await eolManager.planEndOfLife('product1', {
  announcementDate: new Date('2025-06-01'),
  lastSupportDate: new Date('2025-12-31'),
  endOfLifeDate: new Date('2026-12-31'),
  migrationPath: {
    targetProduct: 'product2',
    migrationGuide: 'migration-guide.pdf',
    supportAvailable: true
  },
  disposalProcedures: [
    { type: 'data_sanitization', method: 'cryptographic_erase' },
    { type: 'physical_destruction', method: 'shredding' }
  ],
  communicationPlan: {
    initialNotification: 'eol_announcement',
    regularUpdates: 'monthly',
    finalNotification: 'eol_final'
  }
});

console.log('EOL Plan:', JSON.stringify(eolPlan, null, 2));

// Generate EOL report
const eolReport = eolManager.generateEOLReport();
console.log('EOL Report:', JSON.stringify(eolReport, null, 2));
```

## End-of-Life Checklist

- [ ] EOL planning completed 18-24 months in advance
- [ ] Customer migration paths defined and documented
- [ ] Communication plan established with regular updates
- [ ] Secure data disposal procedures implemented
- [ ] Product information archiving completed
- [ ] New deployment restrictions enforced
- [ ] Support team transition managed
- [ ] Regulatory compliance for EOL processes verified
- [ ] Customer feedback on EOL process collected
- [ ] Post-EOL monitoring and incident response maintained

## Related Standards
- [[Data Disposal]] - Secure data destruction practices
- [[Change Management]] - Controlled system decommissioning
- [[Compliance]] - Regulatory requirements for product lifecycle
- [[Incident Response]] - Post-EOL security monitoring